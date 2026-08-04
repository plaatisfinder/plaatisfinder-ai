from plaatisfinder.database.connection import get_connection


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