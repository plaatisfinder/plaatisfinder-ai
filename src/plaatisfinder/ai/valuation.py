import re
from statistics import median

from plaatisfinder.database.connection import get_connection


MODEL_GROUPS = [
    "2win",
    "roadcruiser",
    "roadcar",
    "summit",
    "campster",
    "vario",
    "duo",
]


VARIANT_WORDS = [
    "plus",
    "shine",
    "prime",
    "r",
    "rs",
    "s",
]


def _normalize(text):
    if not text:
        return ""

    text = text.lower()

    text = text.replace("-", " ")
    text = text.replace("/", " ")

    text = re.sub(r"[^a-z0-9äöå ]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def _tokens(title):
    text = _normalize(title)

    return set(text.split())


def _model_family(title):
    tokens = _tokens(title)

    for model in MODEL_GROUPS:
        if model in tokens:
            return model

    return None


def _variant_tokens(title):
    tokens = _tokens(title)

    return {
        token
        for token in VARIANT_WORDS
        if token in tokens
    }


def _model_score(title_a, title_b):
    family_a = _model_family(title_a)
    family_b = _model_family(title_b)

    if not family_a or not family_b:
        return 0.0

    if family_a != family_b:
        return 0.0

    score = 0.60

    variants_a = _variant_tokens(title_a)
    variants_b = _variant_tokens(title_b)

    if variants_a and variants_b:

        intersection = variants_a & variants_b

        if intersection:
            score += 0.30

    elif not variants_a and not variants_b:

        score += 0.20

    return min(score, 1.0)


def _year_score(year_a, year_b):

    if not year_a or not year_b:
        return 0.5

    difference = abs(year_a - year_b)

    if difference == 0:
        return 1.0

    if difference == 1:
        return 0.90

    if difference == 2:
        return 0.65

    if difference == 3:
        return 0.35

    if difference == 4:
        return 0.15

    return 0.02

def _mileage_score(km_a, km_b):

    if not km_a or not km_b:
        return 0.50

    difference = abs(km_a - km_b)

    if difference <= 10000:
        return 1.00

    if difference <= 25000:
        return 0.85

    if difference <= 50000:
        return 0.65

    if difference <= 75000:
        return 0.40

    if difference <= 100000:
        return 0.20

    return 0.05


def _similarity_score(ad, candidate):

    model = _model_score(
        ad["title"],
        candidate["title"],
    )

    year = _year_score(
        ad["year"],
        candidate["year"],
    )

    mileage = _mileage_score(
        ad["mileage"],
        candidate["mileage"],
    )

    return (
        model * 0.50
        + year * 0.35
        + mileage * 0.15
    )


def find_similar_ads(ad, minimum_score=0.50):

    conn = get_connection()

    candidates = conn.execute(
        """
        SELECT
            url,
            title,
            brand,
            price,
            mileage,
            year,
            source
        FROM ads
        WHERE active=1
          AND price > 0
          AND brand=?
          AND url != ?
        """,
        (
            ad["brand"],
            ad["url"],
        ),
    ).fetchall()

    conn.close()

    similar = []

    for candidate in candidates:

        score = _similarity_score(
            ad,
            candidate,
        )

        if score < minimum_score:
            continue

        item = dict(candidate)

        item["similarity"] = round(
            score,
            3,
        )

        similar.append(item)

    similar.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return similar


def _weighted_median(items):

    if not items:
        return None

    items = sorted(
        items,
        key=lambda item: item["price"],
    )

    total_weight = sum(
        item["weight"]
        for item in items
    )

    target = total_weight / 2

    accumulated = 0

    for item in items:

        accumulated += item["weight"]

        if accumulated >= target:
            return item["price"]

    return items[-1]["price"]


def estimate_market_price(ad):

    similar = find_similar_ads(ad)

    if not similar:

        return {
            "market_price": None,
            "low_price": None,
            "high_price": None,
            "similar_count": 0,
            "confidence": "low",
            "price_difference": None,
            "price_difference_percent": None,
        }

    # Använd de bästa jämförelserna först.
    strong = similar[:10]

    weighted = []

    for item in strong:

        weight = max(
            item["similarity"],
            0.01,
        )

        weighted.append(
            {
                "price": item["price"],
                "weight": weight,
            }
        )

    market_price = _weighted_median(
        weighted
    )

    prices = [
        item["price"]
        for item in strong
    ]

    # Använd percentiler-ish genom att sortera
    # och ta bort ytterligheter när vi har
    # tillräckligt många jämförelser.

    sorted_prices = sorted(prices)

    if len(sorted_prices) >= 5:

        low_prices = sorted_prices[1:-1]

    else:

        low_prices = sorted_prices

    low_price = min(low_prices)
    high_price = max(low_prices)

    difference = (
        ad["price"] - market_price
    )

    difference_percent = (
        difference
        / market_price
        * 100
    )

    count = len(similar)

    if count >= 10:

        confidence = "high"

    elif count >= 5:

        confidence = "medium"

    else:

        confidence = "low"

    return {
        "market_price": round(market_price),
        "low_price": round(low_price),
        "high_price": round(high_price),
        "similar_count": count,
        "confidence": confidence,
        "price_difference": round(
            difference
        ),
        "price_difference_percent": round(
            difference_percent,
            1,
        ),
    }


def analyze_ad(ad):

    valuation = estimate_market_price(ad)

    market_price = valuation["market_price"]

    if market_price is None:

        valuation["verdict"] = (
            "INSUFFICIENT DATA"
        )

        valuation["deal_score"] = None

        return valuation

    difference_percent = (
        valuation[
            "price_difference_percent"
        ]
    )

    if difference_percent <= -15:

        verdict = "EXCEPTIONAL DEAL"
        deal_score = 98

    elif difference_percent <= -10:

        verdict = "EXCELLENT DEAL"
        deal_score = 95

    elif difference_percent <= -5:

        verdict = "GOOD DEAL"
        deal_score = 85

    elif difference_percent <= 3:

        verdict = "FAIR PRICE"
        deal_score = 70

    elif difference_percent <= 10:

        verdict = "EXPENSIVE"
        deal_score = 50

    else:

        verdict = "VERY EXPENSIVE"
        deal_score = 30

    valuation["verdict"] = verdict
    valuation["deal_score"] = deal_score

    return valuation