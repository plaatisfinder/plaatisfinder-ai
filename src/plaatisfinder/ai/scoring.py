from plaatisfinder.ai.rules import (
    score_brand,
    score_model,
    score_price,
    score_year,
    score_mileage,
    score_seller,
)


def score(ad):

    total = 0

    total += score_brand(ad)
    total += score_model(ad)
    total += score_price(ad)
    total += score_year(ad)
    total += score_mileage(ad)
    total += score_seller(ad)

    ad.ai_score = total

    return total