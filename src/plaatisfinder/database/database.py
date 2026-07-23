import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/database.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            url TEXT PRIMARY KEY,
            title TEXT,
            price INTEGER,
            mileage INTEGER,
            year INTEGER,
            location TEXT,
            source TEXT,
            first_seen TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_ad(ad):
    conn = get_connection()

    conn.execute("""
        INSERT OR IGNORE INTO ads
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ad.url,
        ad.title,
        ad.price,
        ad.mileage,
        ad.year,
        ad.location,
        ad.source,
        datetime.now().isoformat(),
    ))

    conn.commit()
    conn.close()