from plaatisfinder.preferences import get_preferences


def score_brand(ad):

    prefs = get_preferences()

    title = ad.title.lower()
    brand = ad.brand.lower()

    for favorite in prefs["brands"]:

        favorite = favorite.lower()

        if favorite in title or favorite in brand:
            return 15

    return 0


def score_model(ad):

    prefs = get_preferences()

    title = ad.title.lower()

    for model in prefs["models"]:

        if model.lower() in title:
            return 20

    return 0


def score_price(ad):

    if ad.price <= 35000:
        return 30

    if ad.price <= 45000:
        return 20

    return 10


def score_year(ad):

    if ad.year >= 2022:
        return 25

    if ad.year >= 2019:
        return 20

    if ad.year >= 2017:
        return 10

    return 0


def score_mileage(ad):

    if ad.mileage == 0:
        return 10

    if ad.mileage <= 50000:
        return 20

    if ad.mileage <= 100000:
        return 15

    if ad.mileage <= 150000:
        return 5

    return 0


def score_seller(ad):

    prefs = get_preferences()

    seller = (ad.seller or "").lower()

    if prefs["seller_type"] == "dealer":

        if "private" not in seller:
            return 10

        return 0

    if prefs["seller_type"] == "private":

        if "private" in seller:
            return 10

        return 0

    return 5