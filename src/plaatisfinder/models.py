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

    # Basfordon
    base_vehicle: str = ""

    # Motor
    engine_size: float = 0.0
    engine_power: int = 0
    engine_model: str = ""

    # Utsläpp
    euro_class: str = ""

    # AdBlue
    # True  = verifierat med AdBlue
    # False = verifierat utan AdBlue
    # None  = okänt
    adblue: bool | None = None

    # Hur säker vi är på AdBlue-informationen
    # "verified", "likely", "unknown"
    adblue_confidence: str = "unknown"