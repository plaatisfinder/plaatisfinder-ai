from plaatisfinder.database.connection import get_connection


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