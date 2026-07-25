from plaatisfinder.scrapers.nettikaravaani import NettikaravaaniScraper
from plaatisfinder.scrapers.caraworld import CaraworldScraper


class ScraperManager:

    def __init__(self):

        self.scrapers = [
            NettikaravaaniScraper(),
            CaraworldScraper(),
        ]

    def get_ads(self):

        ads = []

        for scraper in self.scrapers:

            print(f"Kör {scraper.__class__.__name__}")

            ads.extend(scraper.get_ads())

        return ads