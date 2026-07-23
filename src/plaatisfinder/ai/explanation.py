from plaatisfinder.models import CamperAd


def explain(ad: CamperAd):
    reasons = []

    if ad.price < 40000:
        reasons.append("✅ Bra pris")

    if ad.year >= 2020:
        reasons.append("✅ Modern årsmodell")

    if ad.mileage < 90000:
        reasons.append("✅ Rimlig körsträcka")

    if ad.price > 42000:
        reasons.append("⚠ Relativt högt pris")

    return reasons