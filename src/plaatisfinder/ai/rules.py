from plaatisfinder.preferences import get_preferences


def score_price(ad):
    if ad.price <= 35000:
        return 30
    elif ad.price <= 45000:
        return 20
    return 10


def score_year(ad):
    if ad.year >= 2022:
        return 25
    elif ad.year >= 2019:
        return 20
    elif ad.year >= 2017:
        return 10
    return 0


def score_mileage(ad):
    if ad.mileage == 0:
        return 10

    if ad.mileage <= 50000:
        return 20
    elif ad.mileage <= 100000:
        return 15
    elif ad.mileage <= 150000:
        return 5

    return 0


def score_seller(ad):
    prefs = get_preferences()

    seller = ad.seller.lower()

    if prefs["seller_type"] == "dealer":
        if "private" not in seller:
            return 10
        return 0

    if prefs["seller_type"] == "private":
        if "private" in seller:
            return 10
        return 0

    return 5