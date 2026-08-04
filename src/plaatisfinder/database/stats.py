from plaatisfinder.database.connection import get_connection


def get_statistics():

    conn = get_connection()

    stats = {}

    stats["total"] = conn.execute("""
        SELECT COUNT(*)
        FROM ads
        WHERE active=1
    """).fetchone()[0]

    stats["favorites"] = conn.execute("""
        SELECT COUNT(*)
        FROM ads
        WHERE favorite=1
          AND active=1
    """).fetchone()[0]

    stats["high_ai"] = conn.execute("""
        SELECT COUNT(*)
        FROM ads
        WHERE ai_score>=90
          AND active=1
    """).fetchone()[0]

    stats["average_price"] = conn.execute("""
        SELECT ROUND(AVG(price))
        FROM ads
        WHERE active=1
    """).fetchone()[0] or 0

    stats["new_today"] = conn.execute("""
        SELECT COUNT(*)
        FROM ads
        WHERE date(first_seen)=date('now')
          AND active=1
    """).fetchone()[0]

    stats["price_drops"] = conn.execute("""
        SELECT COUNT(*)
        FROM ads a
        WHERE EXISTS (
            SELECT 1
            FROM price_history p1
            JOIN price_history p2
              ON p1.url=p2.url
            WHERE p1.url=a.url
        )
    """).fetchone()[0]

    conn.close()

    return stats