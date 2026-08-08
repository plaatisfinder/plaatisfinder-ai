import re

import requests
from bs4 import BeautifulSoup

from plaatisfinder.models import CamperAd
from plaatisfinder.scrapers.base import BaseScraper
from plaatisfinder.utils.engine_parser import parse_engine_info


class CaraworldScraper(BaseScraper):

    URL = (
        "https://www.caraworld.de/wohnmobile/"
        "fahrzeugzustand/gebrauchtfahrzeug/"
        "aufbauart/campervan"
    )

    # Tillfälligt 1 sida under test.
    # Ändra tillbaka till 100 när allt fungerar.
    MAX_PAGES = 1

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/138.0 Safari/537.36"
        )
    }

    def get_page(self, page):

        if page == 1:
            url = self.URL
        else:
            url = self.URL + f"/seite-{page}.html"

        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=30,
        )

        print(
            f"Caraworld sida {page}: "
            f"{response.status_code}"
        )

        return response

    def get_detail_info(self, url, year=0):

        if not url:
            return {}

        try:

            response = requests.get(
                url,
                headers=self.HEADERS,
                timeout=30,
            )

            if response.status_code != 200:

                print(
                    f"Detaljsida misslyckades: "
                    f"{response.status_code}"
                )

                return {}

            soup = BeautifulSoup(
                response.text,
                "lxml",
            )

            text = soup.get_text(
                " ",
                strip=True,
            )

            return parse_engine_info(
                text,
                year=year,
            )

        except Exception as e:

            print(
                "Fel vid hämtning av detaljsida:",
                e,
            )

            return {}

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

            print(
                f"Sida {page}: "
                f"{len(cars)} annonser"
            )

            for car in cars:

                try:

                    # --------------------------------
                    # TITEL
                    # --------------------------------

                    title_tag = car.select_one(
                        "h2[itemprop='name']"
                    )

                    if not title_tag:
                        continue

                    title = title_tag.get_text(
                        strip=True
                    )

                    # --------------------------------
                    # PRIS
                    # --------------------------------

                    price_tag = car.select_one(
                        "meta[itemprop='price']"
                    )

                    if not price_tag:
                        continue

                    price = int(
                        price_tag["content"]
                    )

                    # --------------------------------
                    # MÄRKE
                    # --------------------------------

                    brand = ""

                    brand_tag = car.select_one(
                        "meta[itemprop='brand']"
                    )

                    if brand_tag:

                        brand = brand_tag.get(
                            "content",
                            "",
                        )

                    # --------------------------------
                    # ÅR
                    # --------------------------------

                    year = 0

                    year_tag = car.select_one(
                        "meta[itemprop='vehicleModelDate']"
                    )

                    if year_tag:

                        try:

                            year = int(
                                year_tag["content"]
                            )

                        except (
                            ValueError,
                            TypeError,
                        ):

                            year = 0

                    # --------------------------------
                    # MILTAL
                    # --------------------------------

                    mileage = 0

                    for info in car.select(
                        ".cd-outerspace-bottom-small"
                    ):

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

                                mileage = int(
                                    digits
                                )

                    # --------------------------------
                    # URL
                    # --------------------------------

                    url = ""

                    link = car.select_one(
                        "a.cw-fzg-link"
                    )

                    if link:

                        href = link.get(
                            "href",
                            "",
                        )

                        if href.startswith("/"):
                            url = (
                                "https://www.caraworld.de"
                                + href
                            )

                        else:
                            url = href

                    # --------------------------------
                    # DETALJSIDA / MOTORINFO
                    # --------------------------------

                    engine_info = (
                        self.get_detail_info(
                            url,
                            year=year,
                        )
                    )

                    print(
                        "Motorinfo:",
                        engine_info,
                    )

                    # --------------------------------
                    # SÄLJARE
                    # --------------------------------

                    dealer = ""

                    strong = car.select_one(
                        "strong"
                    )

                    if strong:

                        dealer = strong.get_text(
                            strip=True
                        )

                    # --------------------------------
                    # BILD
                    # --------------------------------

                    image_url = ""

                    source = car.select_one(
                        "picture source"
                    )

                    if source:

                        image_url = source.get(
                            "data-srcset",
                            "",
                        )

                    # --------------------------------
                    # FORDONSTYP
                    # --------------------------------

                    vehicle_type = "motorhome"

                    listing_text = (
                        f"{brand} {title}"
                    ).lower()

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
                        keyword in listing_text
                        for keyword
                        in campervan_keywords
                    ):

                        vehicle_type = "campervan"

                    # --------------------------------
                    # ANNONS
                    # --------------------------------

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

                            base_vehicle=engine_info.get(
                                "base_vehicle",
                                "",
                            ),

                            engine_size=engine_info.get(
                                "engine_size",
                                0.0,
                            ),

                            engine_power=engine_info.get(
                                "engine_power",
                                0,
                            ),

                            engine_model=engine_info.get(
                                "engine_model",
                                "",
                            ),

                            euro_class=engine_info.get(
                                "euro_class",
                                "",
                            ),

                            adblue=engine_info.get(
                                "adblue",
                                None,
                            ),

                            adblue_confidence=(
                                engine_info.get(
                                    "adblue_confidence",
                                    "unknown",
                                )
                            ),
                        )
                    )

                except Exception as e:

                    print(
                        "Fel:",
                        e,
                    )

                    continue

            page += 1

        print(
            f"Hämtade {len(ads)} "
            f"annonser från Caraworld"
        )

        return ads