from fastapi import FastAPI, HTTPException
from typing import List

from .db import init_db, get_conn, row_to_item
from .schemas import ItemCreate, ItemUpdate, ItemOut


app = FastAPI(
    title="TODO Service",
    version="1.0.0",
    description="Простой TODO-сервис на FastAPI с SQLite"
)


# Инициализация базы при запуске приложения
@app.on_event("startup")
def startup_event():
    init_db()


# ---------- CREATE ----------
@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate):
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO items (title, description, completed)
            VALUES (?, ?, ?)
            """,
            (payload.title, payload.description, 0)
        )
        conn.commit()

        item_id = cur.lastrowid
        row = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()

    return row_to_item(row)


# ---------- READ (list) ----------
@app.get("/items", response_model=List[ItemOut])
def list_items():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM items ORDER BY id DESC"
        ).fetchall()

    return [row_to_item(r) for r in rows]


# ---------- READ (one item) ----------
@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    return row_to_item(row)


# ---------- UPDATE ----------
@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemUpdate):
    with get_conn() as conn:

        # Проверяем, существует ли объект
        row = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Item not found")

        current = row_to_item(row)

        # Обновляем только переданные значения
        new_title = payload.title or current["title"]
        new_desc = payload.description if payload.description is not None else current["description"]
        new_completed = payload.completed if payload.completed is not None else current["completed"]

        conn.execute(
            """
            UPDATE items
            SET title = ?, description = ?, completed = ?
            WHERE id = ?
            """,
            (new_title, new_desc, int(new_completed), item_id)
        )
        conn.commit()

        # Получаем обновлённую запись
        updated = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()

    return row_to_item(updated)


# ---------- DELETE ----------
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Item not found")

        conn.execute(
            "DELETE FROM items WHERE id = ?",
            (item_id,)
        )
        conn.commit()

    return None
