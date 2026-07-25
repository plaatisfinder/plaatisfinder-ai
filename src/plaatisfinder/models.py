from dataclasses import dataclass


@dataclass
class CamperAd:
    title: str
    price: int
    mileage: int
    year: int
    location: str
    url: str
    source: str
    seller_type: str = "unknown"

    @property
    def ad_id(self) -> str:
        return self.url