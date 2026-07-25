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

    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            url TEXT,
            price INTEGER,
            seen_at TEXT
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

    conn.execute("""
        INSERT INTO price_history
        VALUES (?, ?, ?)
    """, (
        ad.url,
        ad.price,
        datetime.now().isoformat(),
    ))

    conn.commit()
    conn.close()


def get_latest_price(url):
    conn = get_connection()

    row = conn.execute("""
        SELECT price
        FROM price_history
        WHERE url = ?
        ORDER BY seen_at DESC
        LIMIT 1
    """, (url,)).fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]


def has_price_changed(ad):
    latest = get_latest_price(ad.url)

    if latest is None:
        return False

    return latest != ad.price