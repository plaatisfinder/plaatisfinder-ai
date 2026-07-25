from plaatisfinder.models import CamperAd
from plaatisfinder.preferences import get_preferences


def is_interesting(ad: CamperAd) -> bool:

    prefs = get_preferences()

    title = ad.title.lower()
    brand = ad.brand.lower()

    # Märke
    if prefs["brands"]:
        if not any(
            b.lower() in title or b.lower() in brand
            for b in prefs["brands"]
        ):
            return False

    # Modell
    if prefs["models"]:
        if not any(
            m.lower() in title
            for m in prefs["models"]
        ):
            return False

    # Pris
    if ad.price > prefs["max_price"]:
        return False

    # Årsmodell
    if ad.year and ad.year < prefs["min_year"]:
        return False

    # Körsträcka
    if ad.mileage and ad.mileage > prefs["max_mileage"]:
        return False

    # Företag / Privat
    seller_pref = prefs["seller_type"]

    if seller_pref != "any":

        seller = ad.seller.lower()

        is_private = "private" in seller or "privat" in seller

        if seller_pref == "dealer" and is_private:
            return False

        if seller_pref == "private" and not is_private:
            return False

    return True