from plaatisfinder.database.connection import get_connection


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