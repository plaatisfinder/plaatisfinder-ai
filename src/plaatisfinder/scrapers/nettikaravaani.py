import json

import requests
from bs4 import BeautifulSoup

from plaatisfinder.models import CamperAd
from plaatisfinder.scrapers.base import BaseScraper


class NettikaravaaniScraper(BaseScraper):

    BASE_URL = (
        "https://www.nettikaravaani.com/"
        "pikalinkit/retkeilyautot"
        "?latest=update&ord=ASC&page={}&sortCol=datecreate"
    )

    def get_ads(self):

        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/138.0 Safari/537.36"
        }

        ads = []

        for page in range(1, 100):

            print(f"Nettikaravaani sida {page}")

            response = requests.get(
                self.BASE_URL.format(page),
                headers=headers,
                timeout=30,
            )

            print(f"Status: {response.status_code}")

            soup = BeautifulSoup(
                response.text,
                "lxml",
            )

            page_ads = 0

            image_map = {}

            for script in soup.select('script[type="application/ld+json"]'):

                try:
                    data = json.loads(script.string)
                except Exception:
                    continue

                items = (
                    data.get("mainEntity", {})
                        .get("itemListElement", [])
                )

                for item in items:

                    vehicle = item.get("item", {})

                    url = vehicle.get("url", "")
                    image = vehicle.get("image", "")

                    if url and image:

                        ad_id = url.rstrip("/").split("/")[-1]

                        image_map[ad_id] = image

            for tag in soup.select("[data-datalayer]"):

                raw = tag.get("data-datalayer")

                if not raw:
                    continue

                try:
                    data = json.loads(raw)
                except Exception:
                    continue

                brand = data.get("item_brand", "")
                title = data.get("item_name", "")
                seller = data.get("item_seller", "")
                year = data.get("item_year_model") or 0
                price = data.get("item_vehicle_price") or 0
                mileage = data.get("item_mileage") or 0

                try:
                    price = int(price)
                except Exception:
                    continue

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

                if not href:
                    continue

                ad_id = href.rstrip("/").split("/")[-1]

                image_url = image_map.get(ad_id, "")

                if price < 5000:
                    continue

                print(f"{brand} | {title}")

                if any(a.url == href for a in ads):
                    continue

                page_ads += 1

                ads.append(
                    CamperAd(
                        title=title,
                        price=price,
                        mileage=mileage,
                        year=int(year) if year else 0,
                        location="Finland",
                        url=href,
                        source="Nettikaravaani",
                        brand=brand,
                        seller=seller,
                        vehicle_type="campervan",
                        image_url=image_url,
                    )
                )

            print(f"Sida {page}: {page_ads} annonser")

            if page_ads == 0:
                print("Inga fler nya annonser.")
                break

        print(f"Hämtade {len(ads)} annonser från Nettikaravaani")

        return ads