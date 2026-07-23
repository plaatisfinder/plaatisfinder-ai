from plaatisfinder.models import CamperAd
from plaatisfinder.ai.rules import (
    mileage_rule,
    price_rule,
    year_rule,
)


def score(ad: CamperAd) -> int:
    points = 50

    points += price_rule(ad)
    points += mileage_rule(ad)
    points += year_rule(ad)

    return min(points, 100)