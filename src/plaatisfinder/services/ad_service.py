from plaatisfinder.database.database import get_connection


ALLOWED_SORT_COLUMNS = {
    "first_seen",
    "price",
    "year",
    "mileage",
    "ai_score",
}


def get_all_ads(sort="first_seen"):

    if sort not in ALLOWED_SORT_COLUMNS:
        sort = "first_seen"

    conn = get_connection()

    ads = conn.execute(
        f"""
        SELECT *
        FROM ads
        ORDER BY {sort} DESC
        """
    ).fetchall()

    conn.close()

    return ads

from plaatisfinder.database.database import get_ad


def get_ad_by_url(url):

    return get_ad(url)