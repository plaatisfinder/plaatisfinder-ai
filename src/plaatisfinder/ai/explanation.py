from plaatisfinder.ai.rules import (
    score_price,
    score_year,
    score_mileage,
    score_seller,
)


def explain(ad):

    reasons = []

    p = score_price(ad)
    y = score_year(ad)
    m = score_mileage(ad)
    s = score_seller(ad)

    if p == 30:
        reasons.append("💶 +30 Mycket bra pris")
    elif p == 20:
        reasons.append("💶 +20 Bra pris")
    elif p == 10:
        reasons.append("💶 +10 Relativt högt pris")

    if y == 25:
        reasons.append("📅 +25 Mycket modern")
    elif y == 20:
        reasons.append("📅 +20 Modern årsmodell")
    elif y == 10:
        reasons.append("📅 +10 Äldre årsmodell")

    if m == 20:
        reasons.append("🛣️ +20 Låg körsträcka")
    elif m == 15:
        reasons.append("🛣️ +15 Rimlig körsträcka")
    elif m == 10:
        reasons.append("🛣️ +10 Körsträcka ok eller saknas")
    elif m == 5:
        reasons.append("🛣️ +5 Hög körsträcka")

    if s == 10:
        reasons.append("🏢 +10 Matchar önskad säljartyp")
    elif s == 5:
        reasons.append("👤 +5 Neutral säljartyp")

    return reasons