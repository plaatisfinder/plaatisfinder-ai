from plaatisfinder.models import CamperAd


def price_rule(ad: CamperAd) -> int:
    if ad.price <= 38000:
        return 20

    if ad.price <= 40000:
        return 10

    return 0


def mileage_rule(ad: CamperAd) -> int:
    if ad.mileage <= 80000:
        return 20

    if ad.mileage <= 100000:
        return 10

    return 0


def year_rule(ad: CamperAd) -> int:
    if ad.year >= 2021:
        return 20

    if ad.year >= 2019:
        return 10

    return 0