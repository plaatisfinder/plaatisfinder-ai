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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            price INTEGER,
            checked_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def ad_exists(url: str) -> bool:
    conn = get_connection()

    cursor = conn.execute(
        "SELECT 1 FROM ads WHERE url = ?",
        (url,),
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


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
        INSERT INTO price_history (
            url,
            price,
            checked_at
        )
        VALUES (?, ?, ?)
    """, (
        ad.url,
        ad.price,
        datetime.now().isoformat(),
    ))

    conn.commit()
    conn.close()


def get_price(url: str):
    conn = get_connection()

    cursor = conn.execute(
        "SELECT price FROM ads WHERE url = ?",
        (url,),
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None


def update_price(ad):
    conn = get_connection()

    conn.execute("""
        UPDATE ads
        SET price = ?
        WHERE url = ?
    """, (
        ad.price,
        ad.url,
    ))

    conn.execute("""
        INSERT INTO price_history (
            url,
            price,
            checked_at
        )
        VALUES (?, ?, ?)
    """, (
        ad.url,
        ad.price,
        datetime.now().isoformat(),
    ))

    conn.commit()
    conn.close()


def latest_price(url: str):
    conn = get_connection()

    cursor = conn.execute("""
        SELECT price
        FROM price_history
        WHERE url = ?
        ORDER BY id DESC
        LIMIT 1
    """, (url,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None