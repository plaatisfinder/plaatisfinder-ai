from plaatisfinder.services.scanner import scan
from plaatisfinder.ai.scoring import score
from plaatisfinder.ai.explanation import explain


def print_ad(ad, heading):

    print("=" * 60)
    print(heading)
    print()

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


def main():

    print("🚐 PlaatisFinder\n")

    new_ads, changed_ads = scan()

    for i, ad in enumerate(new_ads, start=1):
        print_ad(ad, f"🆕 Ny annons #{i}")

    for ad, old_price in changed_ads:
        print("=" * 60)
        print("📉 Pris sänkt!")
        print()
        print(f"🚐 {ad.title}")
        print(f"💶 {old_price} € → {ad.price} €")
        print()

    print("=" * 60)
    print("KLART")
    print(f"Nya annonser: {len(new_ads)}")
    print(f"Prisändringar: {len(changed_ads)}")


if __name__ == "__main__":
    main()