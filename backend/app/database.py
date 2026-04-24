import sqlite3
import os
import pathlib

DATABASE_PATH = os.getenv("DATABASE_URL", "./data/storyvault.db")

pathlib.Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = get_db()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS journals (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                content     TEXT NOT NULL,
                category    TEXT NOT NULL CHECK(category IN ('tech','work','life','fun')),
                vocab_words TEXT,
                score       INTEGER,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS stories (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                content     TEXT NOT NULL,
                category    TEXT NOT NULL CHECK(category IN ('tech','work','life','fun')),
                themes      TEXT,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS writing_streak (
                id          TEXT PRIMARY KEY,
                date        TEXT NOT NULL UNIQUE,
                type        TEXT NOT NULL CHECK(type IN ('journal','story'))
            );
        """)
        conn.commit()
    finally:
        conn.close()
