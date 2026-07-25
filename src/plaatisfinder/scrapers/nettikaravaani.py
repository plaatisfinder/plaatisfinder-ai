import json
import re

import requests
from bs4 import BeautifulSoup

from plaatisfinder.models import CamperAd


class NettikaravaaniScraper:

    URL = "https://www.nettikaravaani.com/hakutulokset"

    def get_ads(self):

        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/138.0 Safari/537.36"
        }

        response = requests.get(
            self.URL,
            headers=headers,
            timeout=30,
        )

        print(f"Nettikaravaani status: {response.status_code}")

        soup = BeautifulSoup(response.text, "lxml")

        ads = []

        for tag in soup.select("[data-datalayer]"):

            raw = tag.get("data-datalayer")

            if not raw:
                continue

            try:
                data = json.loads(raw)
            except Exception:
                continue

            brand = data.get("item_brand", "")
            variant = data.get("item_variant") or ""
            title = data.get("item_name", "")
            seller = data.get("item_seller", "")
            year = data.get("item_year_model") or 0
            price = data.get("item_vehicle_price") or 0
            mileage = data.get("item_mileage") or 0

            try:
                mileage = int(mileage)
            except Exception:
                mileage = 0

            href = ""

            link = tag.find("a", href=True)
            if link:
                href = link["href"]

            if href.startswith("/"):
                href = "https://www.nettikaravaani.com" + href

            ads.append(
                CamperAd(
                    title=title,
                    price=int(price),
                    mileage=mileage,
                    year=int(year) if year else 0,
                    location="Finland",
                    url=href,
                    source="Nettikaravaani",
                    brand=brand,
                    seller=seller,
                )
            )

        print(f"Hämtade {len(ads)} annonser från Nettikaravaani")

        return ads