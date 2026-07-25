from plaatisfinder.models import CamperAd
from plaatisfinder.scrapers.base import BaseScraper


class MockScraper(BaseScraper):

    def get_ads(self):

        return [
            CamperAd(
                title="Adria Twin 600 SP",
                price=39900,
                mileage=82000,
                year=2020,
                location="Hamburg",
                url="https://example.com",
                source="Mock",
                seller_type="dealer",
            )
        ]