import re

import requests
from bs4 import BeautifulSoup

from plaatisfinder.models import CamperAd
from plaatisfinder.scrapers.base import BaseScraper


class CaraworldScraper(BaseScraper):

    URL = "https://www.caraworld.de/wohnmobile/fahrzeugzustand/gebrauchtfahrzeug"

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

        print(f"Caraworld status: {response.status_code}")

        soup = BeautifulSoup(response.text, "lxml")

        ads = []

        for car in soup.select('div[itemtype="https://schema.org/Car"]'):

            try:

                title = car.select_one(
                    "h2[itemprop='name']"
                ).get_text(strip=True)

                price = int(
                    car.select_one(
                        "meta[itemprop='price']"
                    )["content"]
                )

                brand = car.select_one(
                    "meta[itemprop='brand']"
                )["content"]

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

                        mileage = int(
                            re.sub(
                                r"\D",
                                "",
                                value.text,
                            )
                        )

                link = car.select_one("a.cw-fzg-link")

                url = ""

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
                    )
                )

            except Exception:
                continue

        print(f"Hämtade {len(ads)} annonser från Caraworld")

        return ads