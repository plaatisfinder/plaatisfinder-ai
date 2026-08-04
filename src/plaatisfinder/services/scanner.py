from plaatisfinder.database.database import (
    ad_exists,
    create_tables,
    get_price,
    save_ad,
    update_price,
    mark_all_inactive,
    mark_active,
)
from plaatisfinder.filters import is_interesting
from plaatisfinder.scrapers.manager import ScraperManager
from plaatisfinder.ai.scoring import score


def scan():

    create_tables()

    # Alla annonser markeras först som inaktiva
    mark_all_inactive()

    manager = ScraperManager()

    ads = manager.get_ads()

    ads = [
        ad
        for ad in ads
        if is_interesting(ad)
    ]

    ads = sorted(
        ads,
        key=score,
        reverse=True,
    )

    new_ads = []
    changed_ads = []

    for ad in ads:

        if not ad_exists(ad.url):

            save_ad(ad)

            new_ads.append(ad)

        else:

            mark_active(ad.url)

            old_price = get_price(ad.url)

            if old_price != ad.price:

                update_price(ad)

                changed_ads.append(
                    (
                        ad,
                        old_price,
                    )
                )

    return new_ads, changed_ads