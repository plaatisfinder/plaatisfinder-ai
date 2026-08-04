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

    brand: str = ""
    seller: str = ""

    image_url: str = ""

    vehicle_type: str = "unknown"

    ai_score: int = 0