import os
import sqlite3
from contextlib import contextmanager

# Папка, где будет храниться база внутри контейнера
DATA_DIR = os.getenv("DATA_DIR", "/app/data")
DB_PATH = os.getenv("DB_PATH", os.path.join(DATA_DIR, "todo.db"))


def init_db() -> None:
    """
    Создаёт директорию под базу и таблицу items, если она ещё не существует.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


@contextmanager
def get_conn():
    """
    Контекстный менеджер для безопасного подключения к SQLite.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def row_to_item(row) -> dict:
    """
    Преобразует запись SQLite в dict, удобный для ItemOut.
    """
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"]),
        "created_at": row["created_at"]
    }
