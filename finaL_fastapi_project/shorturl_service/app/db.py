import os
import sqlite3
from contextlib import contextmanager

# Папка, где будет жить база данных
DATA_DIR = os.getenv("DATA_DIR", "/app/data")
DB_PATH = os.getenv("DB_PATH", os.path.join(DATA_DIR, "shorturl.db"))


def init_db() -> None:
    """
    Создаёт директорию и таблицу links, если её нет.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT UNIQUE NOT NULL,
                full_url TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


@contextmanager
def get_conn():
    """
    Контекстный менеджер для подключения к SQLite.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def row_to_link(row) -> dict:
    """
    Преобразует строку из базы в dict.
    """
    return {
        "id": row["id"],
        "short_id": row["short_id"],
        "full_url": row["full_url"],
        "clicks": row["clicks"],
        "created_at": row["created_at"]
    }
