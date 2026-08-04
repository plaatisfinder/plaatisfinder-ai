import sqlite3

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from plaatisfinder.utils.date_utils import days_online

from plaatisfinder.database.stats import get_statistics

from plaatisfinder.database.ads import get_ad

from plaatisfinder.database.history import (
    get_previous_price,
    get_price_history,
)

from plaatisfinder.database.favorites import (
    is_favorite,
    set_favorite,
)

from plaatisfinder.database.watches import (
    add_watch,
    get_watches,
)

app = Flask(__name__)

@app.route("/watches")
def watches():

    watches = get_watches()

    return render_template(
        "watches.html",
        watches=watches,
    )

@app.route("/watch/new", methods=["GET", "POST"])
def new_watch():

    if request.method == "POST":

        add_watch(

            request.form["brand"],

            int(request.form["min_ai"]),

            int(request.form["max_price"]),

            int(request.form["min_year"]),

            int(request.form["max_mileage"]),

        )

        return redirect(url_for("watches"))

    return render_template(
        "watch_form.html",
    )


def get_connection():

    conn = sqlite3.connect("data/database.db")
    conn.row_factory = sqlite3.Row

    return conn

def get_brands():

    conn = get_connection()

    brands = conn.execute(
        """
        SELECT
            brand,
            COUNT(*) AS total

        FROM ads

        WHERE active=1
          AND brand IS NOT NULL
          AND brand <> ''

        GROUP BY brand

        ORDER BY brand
        """
    ).fetchall()

    conn.close()

    return brands


def get_ads():

    sort = request.args.get("sort", "ai_score")

    year_from = int(request.args.get("year_from", 2015))
    year_to = int(request.args.get("year_to", 2030))

    price_from = int(request.args.get("price_from", 0))
    price_to = int(request.args.get("price_to", 45000))

    km_from = int(request.args.get("km_from", 0))
    km_to = int(request.args.get("km_to", 100000))

    favorites_only = request.args.get("favorites") == "1"

    selected_brands = request.args.getlist("brand")

    allowed = {
        "ai_score": "ai_score",
        "price": "price",
        "year": "year",
        "mileage": "mileage",
        "first_seen": "first_seen",
    }

    order = allowed.get(sort, "ai_score")

    where = """

        WHERE active=1

        AND (year=0 OR (year>=? AND year<=?))

        AND price>=?
        AND price<=?

        AND (mileage=0 OR (mileage>=? AND mileage<=?))

    """

    if favorites_only:
        where += "\nAND favorite=1"

    if selected_brands:

        placeholders = ",".join("?" for _ in selected_brands)

        where += f"\nAND brand IN ({placeholders})"

    params = [
        year_from,
        year_to,
        price_from,
        price_to,
        km_from,
        km_to,
    ]

    params.extend(selected_brands)

    conn = get_connection()

    ads = conn.execute(
        f"""
        SELECT *

        FROM ads

        {where}

        ORDER BY {order} DESC
        """,
        params,
    ).fetchall()

    ads = [dict(ad) for ad in ads]

    for ad in ads:

        previous_price = get_previous_price(ad["url"])

        ad["previous_price"] = previous_price

        if previous_price is None:
            ad["price_change"] = 0
        else:
            ad["price_change"] = ad["price"] - previous_price

        ad["days_online"] = days_online(ad["first_seen"])

    conn.close()

    return (
        ads,
        year_from,
        year_to,
        price_from,
        price_to,
        km_from,
        km_to,
        sort,
        favorites_only,
        selected_brands,
    )


@app.route("/favorite/<path:url>")
def favorite(url):

    if is_favorite(url):
        set_favorite(url, 0)
    else:
        set_favorite(url, 1)

    return redirect(url_for("home"))


@app.route("/")
def home():

    (
        ads,
        year_from,
        year_to,
        price_from,
        price_to,
        km_from,
        km_to,
        sort,
        favorites_only,
        selected_brands,
    ) = get_ads()

    brands = get_brands()

    total = len(ads)

    fi = sum(
        1
        for ad in ads
        if ad["source"] == "Nettikaravaani"
    )

    de = sum(
        1
        for ad in ads
        if ad["source"] == "Caraworld"
    )

    stats = get_statistics()

    return render_template(
        "index.html",
        ads=ads,
        total=total,
        fi=fi,
        de=de,
        stats=stats,
        year_from=year_from,
        year_to=year_to,
        price_from=price_from,
        price_to=price_to,
        km_from=km_from,
        km_to=km_to,
        sort=sort,
        favorites_only=favorites_only,
        brands=brands,
        selected_brands=selected_brands,
    )

@app.route("/ad/<path:url>")

def ad_details(url):

    ad = get_ad(url)

    if not ad:
        return "Annonsen hittades inte.", 404

    history = get_price_history(url)

    labels = [
        row["checked_at"][:10]
        for row in reversed(history)
    ]

    prices = [
        row["price"]
        for row in reversed(history)
    ]

    print("labels:", labels)
    print("prices:", prices)

    ad["days_online"] = days_online(ad["first_seen"])

    return render_template(
        "ad.html",
        ad=ad,
        history=history,
        labels=labels,
        prices=prices,
    )

if __name__ == "__main__":
    app.run(debug=True)