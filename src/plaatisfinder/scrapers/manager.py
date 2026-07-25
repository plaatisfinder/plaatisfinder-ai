from plaatisfinder.scrapers.mock import MockScraper


class ScraperManager:

    def __init__(self):
        self.scrapers = [
            MockScraper(),
        ]

    def get_ads(self):

        ads = []

        for scraper in self.scrapers:
            ads.extend(scraper.get_ads())

        return ads