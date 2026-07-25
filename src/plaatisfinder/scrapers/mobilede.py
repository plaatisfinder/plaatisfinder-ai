from plaatisfinder.preferences import get_preferences
from plaatisfinder.models import CamperAd


def get_ads():
    prefs = get_preferences()

    print("Söker efter:")
    print(f"🚐 {prefs['brand']} {prefs['model']}")
    print(f"📅 Min år: {prefs['min_year']}")
    print(f"💶 Maxpris: {prefs['max_price']} €")
    print(f"🛣️ Max mil: {prefs['max_mileage']} km")
    print(f"🏢 Säljare: {prefs['seller_type']}")
    print()

    return [
        CamperAd(
            title="Adria Twin 600 SP",
            price=39900,
            mileage=82000,
            year=2020,
            location="Hamburg",
            url="https://example.com/1",
            source="Mobile.de",
        ),
        CamperAd(
            title="Pössl Roadcruiser",
            price=36900,
            mileage=98000,
            year=2019,
            location="Berlin",
            url="https://example.com/2",
            source="Mobile.de",
        ),
        CamperAd(
            title="Globecar Summit 600",
            price=42900,
            mileage=61000,
            year=2021,
            location="München",
            url="https://example.com/3",
            source="Mobile.de",
        ),
    ]