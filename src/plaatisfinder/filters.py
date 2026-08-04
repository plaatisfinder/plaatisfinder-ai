from plaatisfinder.models import CamperAd
from plaatisfinder.preferences import get_preferences


def is_interesting(ad: CamperAd):

    prefs = get_preferences()

    title = ad.title.lower()
    brand = (ad.brand or "").lower()

    # Märke
    if prefs["brands"]:

        if not any(
            b.lower() in title or b.lower() in brand
            for b in prefs["brands"]
        ):
            return False

    # Endast plåtisar
    if ad.vehicle_type != "campervan":
        return False

    # Företag / Privat
    seller_pref = prefs["seller_type"]

    if seller_pref != "any":

        seller = (ad.seller or "").lower()

        is_private = (
            "private" in seller
            or "privat" in seller
        )

        if seller_pref == "dealer" and is_private:
            return False

        if seller_pref == "private" and not is_private:
            return False

    return True