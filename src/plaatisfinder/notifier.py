import os

import requests

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def euro(value):

    if value is None:
        return "-"

    return f"{value:,}".replace(",", " ")


def send_telegram(message):

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN eller CHAT_ID saknas.")
        return

    response = requests.post(

        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",

        data={

            "chat_id": CHAT_ID,
            "text": message,

        },

        timeout=10,

    )

    if response.status_code != 200:

        print("Telegramfel:")
        print(response.text)


def notify(new_ads, changed_ads):

    print()
    print("=" * 60)
    print("🔔 Sammanfattning")
    print()

    print(f"🆕 Nya annonser: {len(new_ads)}")
    print(f"📉 Prisändringar: {len(changed_ads)}")

    sent = 0

    # ------------------------
    # Nya annonser
    # ------------------------

    for ad in new_ads:

        if ad.ai_score < 80:
            continue

        message = (
            "🆕 Ny annons!\n\n"
            f"🚐 {ad.title}\n\n"
            f"⭐ AI {ad.ai_score}\n"
            f"💶 {euro(ad.price)} €\n"
            f"📅 {ad.year}\n"
            f"🛣️ {euro(ad.mileage)} km\n"
            f"🌍 {ad.source}\n\n"
            f"{ad.url}"
        )

        send_telegram(message)

        sent += 1

    # ------------------------
    # Prissänkningar
    # ------------------------

    for ad, old_price in changed_ads:

        if ad.ai_score < 80:
            continue

        saved = old_price - ad.price

        message = (
            "📉 Prissänkning!\n\n"
            f"🚐 {ad.title}\n\n"
            f"💶 {euro(old_price)} € → {euro(ad.price)} €\n"
            f"💚 Sänkt med {euro(saved)} €\n"
            f"⭐ AI {ad.ai_score}\n"
            f"📅 {ad.year}\n"
            f"🛣️ {euro(ad.mileage)} km\n"
            f"🌍 {ad.source}\n\n"
            f"{ad.url}"
        )

        send_telegram(message)

        sent += 1

    # ------------------------
    # Sammanfattning
    # ------------------------

    if sent > 0:

        summary = (
            "📊 PlaatisFinder\n\n"
            f"📨 Skickade notifieringar: {sent}\n"
            f"🆕 Nya annonser: {len(new_ads)}\n"
            f"📉 Prisändringar: {len(changed_ads)}"
        )

        send_telegram(summary)


if __name__ == "__main__":

    send_telegram("✅ PlaatisFinder Telegram fungerar!")