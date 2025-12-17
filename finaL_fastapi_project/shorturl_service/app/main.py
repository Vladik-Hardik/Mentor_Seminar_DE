from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from typing import List
import string
import random

from .db import init_db, get_conn, row_to_link
from .schemas import URLCreate, URLOut, URLInfo


app = FastAPI(
    title="ShortURL Service",
    description="Сервис сокращения ссылок на FastAPI + SQLite",
    version="1.0.0"
)


#  ИНИЦИАЛИЗАЦИЯ БАЗЫ
@app.on_event("startup")
def startup_event():
    init_db()


#УТИЛИТА ДЛЯ ГЕНЕРАЦИИ short_id
def generate_short_id(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


#СОЗДАНИЕ КОРОТКОЙ ССЫЛКИ
@app.post("/shorten", response_model=URLOut, status_code=201)
def shorten_url(payload: URLCreate):
    short_id = generate_short_id()

    with get_conn() as conn:
        # Проверяем, нет ли коллизий
        while conn.execute("SELECT 1 FROM links WHERE short_id = ?", (short_id,)).fetchone():
            short_id = generate_short_id()

        conn.execute(
            """
            INSERT INTO links (short_id, full_url)
            VALUES (?, ?)
            """,
            (short_id, payload.url)
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM links WHERE short_id = ?",
            (short_id,)
        ).fetchone()

    return row_to_link(row)


# РЕДИРЕКТ ПО КОРОТКОЙ ССЫЛКE 
@app.get("/{short_id}")
def redirect_short(short_id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM links WHERE short_id = ?",
            (short_id,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Short URL not found")

        # Увеличиваем количество переходов
        conn.execute(
            "UPDATE links SET clicks = clicks + 1 WHERE short_id = ?",
            (short_id,)
        )
        conn.commit()

    full_url = row["full_url"]
    return RedirectResponse(full_url)


#  СТАТИСТИКА ПО КОРОТКОЙ ССЫЛКЕ
@app.get("/stats/{short_id}", response_model=URLInfo)
def get_stats(short_id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM links WHERE short_id = ?",
            (short_id,)
        ).fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Short URL not found")

    return row_to_link(row)
