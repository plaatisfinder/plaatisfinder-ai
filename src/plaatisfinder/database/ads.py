from datetime import datetime

from plaatisfinder.database.connection import get_connection


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