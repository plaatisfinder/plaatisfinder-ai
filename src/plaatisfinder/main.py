from plaatisfinder.database.database import (
    create_tables,
    save_ad,
)

from plaatisfinder.scrapers.manager import ScraperManager
from plaatisfinder.ai.scoring import score
from plaatisfinder.ai.explanation import explain


def main():
    create_tables()

    print("🚐 PlaatisFinder\n")

    manager = ScraperManager()
    ads = manager.get_ads()

    ads = sorted(
        ads,
        key=score,
        reverse=True,
    )

    for i, ad in enumerate(ads, start=1):
        save_ad(ad)

        print("=" * 50)
        print(f"#{i}")
        print(f"🚐 {ad.title}")
        print(f"⭐ AI Score: {score(ad)}/100")

        for reason in explain(ad):
            print(reason)

        print(f"💶 Pris: {ad.price} €")
        print(f"🛣️ {ad.mileage} km")
        print(f"📅 {ad.year}")
        print(f"📍 {ad.location}")
        print(f"🌍 {ad.source}")
        print(f"🔗 {ad.url}")
        print()


if __name__ == "__main__":
    main()