import re

import requests
from bs4 import BeautifulSoup

from plaatisfinder.models import CamperAd
from plaatisfinder.scrapers.base import BaseScraper


class CaraworldScraper(BaseScraper):

    URL = "https://www.caraworld.de/wohnmobile/fahrzeugzustand/gebrauchtfahrzeug/aufbauart/campervan"

    MAX_PAGES = 100

    def get_page(self, page):

        if page == 1:
            url = self.URL
        else:
            url = self.URL + f"/seite-{page}.html"

        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/138.0 Safari/537.36"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        print(f"Caraworld sida {page}: {response.status_code}")

        return response

    def get_ads(self):

        ads = []

        page = 1

        while page <= self.MAX_PAGES:

            response = self.get_page(page)

            if response.status_code != 200:
                print("Inga fler sidor.")
                break

            soup = BeautifulSoup(
                response.text,
                "lxml",
            )

            cars = soup.select(
                'div[itemtype="https://schema.org/Car"]'
            )

            if not cars:
                print("Inga fler annonser.")
                break

            print(f"Sida {page}: {len(cars)} annonser")

            for car in cars:

                try:

                    title = car.select_one(
                        "h2[itemprop='name']"
                    ).get_text(strip=True)

                    price = int(
                        car.select_one(
                            "meta[itemprop='price']"
                        )["content"]
                    )

                    brand = ""

                    brand_tag = car.select_one(
                        "meta[itemprop='brand']"
                    )

                    if brand_tag:
                        brand = brand_tag["content"]

                    year = 0

                    year_tag = car.select_one(
                        "meta[itemprop='vehicleModelDate']"
                    )

                    if year_tag:
                        year = int(year_tag["content"])

                    mileage = 0

                    for info in car.select(".cd-outerspace-bottom-small"):

                        label = info.select_one(
                            ".cd-wrapper-suchergebnis-info"
                        )

                        value = info.select_one(
                            ".cd-wrapper-suchergebnis-info-zeile"
                        )

                        if not label or not value:
                            continue

                        if "KM-Stand" in label.text:

                            digits = re.sub(
                                r"\D",
                                "",
                                value.text,
                            )

                            if digits:
                                mileage = int(digits)

                    url = ""

                    link = car.select_one("a.cw-fzg-link")

                    if link:

                        href = link["href"]

                        if href.startswith("/"):
                            url = "https://www.caraworld.de" + href
                        else:
                            url = href

                    dealer = ""

                    strong = car.select_one("strong")

                    if strong:
                        dealer = strong.get_text(strip=True)

                    image_url = ""

                    source = car.select_one("picture source")

                    if source:
                        image_url = source.get("data-srcset", "")

                    vehicle_type = "motorhome"

                    text = f"{brand} {title}".lower()

                    campervan_keywords = [
                        "twin",
                        "roadcruiser",
                        "summit",
                        "carabus",
                        "2 win",
                        "2win",
                        "duo",
                        "duett",
                        "campster",
                        "campervan",
                        "kastenwagen",
                    ]

                    if any(
                        keyword in text
                        for keyword in campervan_keywords
                    ):
                        vehicle_type = "campervan"

                    ads.append(
                        CamperAd(
                            title=title,
                            price=price,
                            mileage=mileage,
                            year=year,
                            location="Germany",
                            url=url,
                            source="Caraworld",
                            brand=brand,
                            seller=dealer,
                            image_url=image_url,
                            vehicle_type=vehicle_type,
                        )
                    )

                except Exception as e:
                    print("Fel:", e)
                    continue

            page += 1

        print(f"Hämtade {len(ads)} annonser från Caraworld")

        return ads