import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/database.db")


def get_connection():

    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def create_tables():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ads (

            url TEXT PRIMARY KEY,

            title TEXT,

            brand TEXT,

            price INTEGER,

            mileage INTEGER,

            year INTEGER,

            location TEXT,

            source TEXT,

            image_url TEXT,

            ai_score INTEGER,

            first_seen TEXT,

            last_seen TEXT,

            active INTEGER DEFAULT 1,

            favorite INTEGER DEFAULT 0

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

    conn.execute("""
        CREATE TABLE IF NOT EXISTS watches (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            brand TEXT,

            min_ai INTEGER,

            max_price INTEGER,

            min_year INTEGER,

            max_mileage INTEGER

        )
    """)

    conn.commit()
    conn.close()


def ad_exists(url):

    conn = get_connection()

    row = conn.execute(
        "SELECT 1 FROM ads WHERE url=?",
        (url,),
    ).fetchone()

    conn.close()

    return row is not None


def save_ad(ad):

    now = datetime.now().isoformat()

    conn = get_connection()

    conn.execute("""
        INSERT OR REPLACE INTO ads
        (
            url,
            title,
            brand,
            price,
            mileage,
            year,
            location,
            source,
            image_url,
            ai_score,
            active,
            first_seen,
            last_seen
        )

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)   
          """, (

        ad.url,
        ad.title,
        ad.brand,
        ad.price,
        ad.mileage,
        ad.year,
        ad.location,
        ad.source,
        ad.image_url,
        ad.ai_score,
        1,
        now,
        now,

    ))

    conn.execute("""
        INSERT INTO price_history
        (
            url,
            price,
            checked_at
        )

        VALUES (?,?,?)
    """, (

        ad.url,
        ad.price,
        now,

    ))

    conn.commit()
    conn.close()


def update_price(ad):

    now = datetime.now().isoformat()

    conn = get_connection()

    conn.execute("""
        UPDATE ads

        SET

            brand=?,
            price=?,
            image_url=?,
            ai_score=?,
            last_seen=?

        WHERE url=?

    """, (

        ad.brand,
        ad.price,
        ad.image_url,
        ad.ai_score,
        now,
        ad.url,

    ))

    conn.execute("""
        INSERT INTO price_history
        (
            url,
            price,
            checked_at
        )

        VALUES (?,?,?)
    """, (

        ad.url,
        ad.price,
        now,

    ))

    conn.commit()
    conn.close()

def get_previous_price(url):

    conn = get_connection()

    row = conn.execute("""
        SELECT price

        FROM price_history

        WHERE url=?

        ORDER BY checked_at DESC

        LIMIT 1 OFFSET 1
    """, (

        url,

    )).fetchone()

    conn.close()

    if row:
        return row["price"]

    return None

def update_last_seen(url):

    conn = get_connection()

    conn.execute("""
        UPDATE ads

        SET last_seen=?

        WHERE url=?
    """, (

        datetime.now().isoformat(),
        url,

    ))

    conn.commit()
    conn.close()


def get_price(url):

    conn = get_connection()

    row = conn.execute(
        "SELECT price FROM ads WHERE url=?",
        (url,),
    ).fetchone()

    conn.close()

    if row:
        return row["price"]

    return None


def latest_price(url):

    conn = get_connection()

    row = conn.execute("""
        SELECT price

        FROM price_history

        WHERE url=?

        ORDER BY id DESC

        LIMIT 1
    """, (

        url,

    )).fetchone()

    conn.close()

    if row:
        return row["price"]

    return None


def get_ad(url):

    conn = get_connection()

    ad = conn.execute(
        """
        SELECT *
        FROM ads
        WHERE url = ?
        """,
        (url,),
    ).fetchone()

    conn.close()

    return ad

def get_price_history(url):

    conn = get_connection()

    history = conn.execute(
        """
        SELECT
            price,
            checked_at

        FROM price_history

        WHERE url=?

        ORDER BY checked_at DESC
        """,
        (url,),
    ).fetchall()

    conn.close()

    return history

def mark_all_inactive():

    conn = get_connection()

    conn.execute("""

        UPDATE ads

        SET active=0

    """)

    conn.commit()
    conn.close()


def mark_active(url):

    conn = get_connection()

    conn.execute("""

        UPDATE ads

        SET

            active=1,
            last_seen=?

        WHERE url=?

    """, (

        datetime.now().isoformat(),
        url,

    ))

    conn.commit()
    conn.close()


def get_active_ads():

    conn = get_connection()

    ads = conn.execute("""

        SELECT *

        FROM ads

        WHERE active=1

        ORDER BY ai_score DESC

    """).fetchall()

    conn.close()

    return ads

def set_favorite(url, favorite):

    conn = get_connection()

    conn.execute(
        """
        UPDATE ads

        SET favorite=?

        WHERE url=?
        """,
        (
            favorite,
            url,
        ),
    )

    conn.commit()
    conn.close()


def is_favorite(url):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT favorite

        FROM ads

        WHERE url=?
        """,
        (url,),
    ).fetchone()

    conn.close()

    if row:
        return bool(row["favorite"])

    return False

def add_watch(

    brand,
    min_ai,
    max_price,
    min_year,
    max_mileage,

):

    conn = get_connection()

    conn.execute("""

        INSERT INTO watches
        (

            brand,
            min_ai,
            max_price,
            min_year,
            max_mileage

        )

        VALUES (?,?,?,?,?)

    """, (

        brand,
        min_ai,
        max_price,
        min_year,
        max_mileage,

    ))

    conn.commit()
    conn.close()

    def get_watches():

        conn = get_connection()

        watches = conn.execute("""

            SELECT *

            FROM watches

            ORDER BY id

        """).fetchall()

        conn.close()

        return watches