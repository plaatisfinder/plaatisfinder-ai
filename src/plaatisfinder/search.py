from urllib.parse import urlencode

from plaatisfinder.preferences import get_preferences


def build_query():

    prefs = get_preferences()

    return {
        "brands": prefs["brands"],
        "models": prefs["models"],
        "max_price": prefs["max_price"],
        "min_year": prefs["min_year"],
        "max_mileage": prefs["max_mileage"],
        "seller_type": prefs["seller_type"],
    }


def build_url(base_url: str, params: dict):

    query = urlencode(params, doseq=True)

    return f"{base_url}?{query}"