import re


def parse_engine_info(text, year=0, base_vehicle=""):
    """
    Försöker hitta motor-, basfordons-, effekt-, Euro- och
    AdBlue-information från annonstext.

    Returnerar ett dictionary som passar CamperAd.
    """

    text = text or ""
    lower = text.lower()

    result = {
        "base_vehicle": base_vehicle or "",
        "engine_size": 0.0,
        "engine_power": 0,
        "engine_model": "",
        "euro_class": "",
        "adblue": None,
        "adblue_confidence": "unknown",
    }

    # --------------------------------------------------
    # BASFORDON
    # --------------------------------------------------

    base_patterns = {
        "Fiat Ducato": [
            r"\bfiat\s+ducato\b",
            r"\bducato\b",
        ],

        "Peugeot Boxer": [
            r"\bpeugeot\s+boxer\b",
            r"\bboxer\b",
        ],

        "Citroën Jumper": [
            r"\bcitro[ëe]n\s+jumper\b",
            r"\bjumper\b",
        ],

        "Ford Transit": [
            r"\bford\s+transit\b",
            r"\btransit\b",
        ],

        "Mercedes Sprinter": [
            r"\bmercedes[- ]benz\s+sprinter\b",
            r"\bsprinter\b",
        ],

        "VW Crafter": [
            r"\bvolkswagen\s+crafter\b",
            r"\bvw\s+crafter\b",
            r"\bcrafter\b",
        ],

        "Renault Master": [
            r"\brenault\s+master\b",
            r"\bmaster\b",
        ],

        "Opel Movano": [
            r"\bopel\s+movano\b",
            r"\bmovano\b",
        ],
    }

    if not result["base_vehicle"]:

        for name, patterns in base_patterns.items():

            if any(
                re.search(pattern, lower)
                for pattern in patterns
            ):
                result["base_vehicle"] = name
                break

    # --------------------------------------------------
    # MOTORSTORLEK
    # --------------------------------------------------

    size_patterns = [
        r"\b(\d[.,]\d)\s*(?:l|liter|litre)\b",

        r"\b(\d[.,]\d)\s*(?:l|liter|litre)"
        r"\s+diesel\b",

        r"\b(\d[.,]\d)\s*"
        r"(?:multijet|bluehdi|hdi|tdi|dci|cdi|ecoblue)\b",
    ]

    for pattern in size_patterns:

        match = re.search(pattern, lower)

        if match:

            result["engine_size"] = float(
                match.group(1).replace(",", ".")
            )

            break

    # --------------------------------------------------
    # MOTOREFFEKT
    # --------------------------------------------------

    # Exempel:
    # 163 PS
    # 150 PS
    # 120 kW
    # 120 kW / 163 PS

    ps_match = re.search(
        r"\b(\d{2,3})\s*(?:ps|hk|hp)\b",
        lower,
    )

    if ps_match:

        result["engine_power"] = int(
            ps_match.group(1)
        )

    else:

        kw_match = re.search(
            r"\b(\d{2,3})\s*kw\b",
            lower,
        )

        if kw_match:

            kw = int(
                kw_match.group(1)
            )

            result["engine_power"] = round(
                kw * 1.35962
            )

    # --------------------------------------------------
    # MOTORFAMILJ
    # --------------------------------------------------

    # Viktigt:
    # längsta/specifikaste först.
    #
    # Annars blir "Multijet II" bara "Multijet".

    engine_patterns = [
        "multijet ii",
        "multijet",
        "bluehdi",
        "ecoblue",
        "hdi",
        "tdi",
        "dci",
        "cdi",
    ]

    for engine in engine_patterns:

        if engine in lower:

            result["engine_model"] = engine.upper()

            break

    # --------------------------------------------------
    # EUROKLASS
    # --------------------------------------------------

    euro_patterns = [
        r"\beuro\s*6d[\-\s]?final\b",
        r"\beuro\s*6d[\-\s]?temp\b",
        r"\beuro\s*6d\b",
        r"\beuro\s*6\b",
        r"\beuro\s*5\b",
        r"\beuro\s*4\b",
    ]

    for pattern in euro_patterns:

        match = re.search(
            pattern,
            lower,
        )

        if match:

            value = match.group(0)

            value = re.sub(
                r"\s+",
                " ",
                value,
            )

            result["euro_class"] = (
                value.title()
            )

            break

    # --------------------------------------------------
    # ADBLUE — VERIFIERAT
    # --------------------------------------------------

    no_adblue_patterns = [
        r"\bohne\s+adblue\b",
        r"\bohne\s+ad[- ]?blue\b",
        r"\bkein\s+adblue\b",
        r"\bkeine\s+adblue\b",
        r"\bohne\s+scr\b",

        r"\bwithout\s+adblue\b",
        r"\bno\s+adblue\b",

        r"\bilman\s+adblue\b",
        r"\bei\s+adblueta\b",
        r"\bei\s+adbluea\b",
    ]

    yes_adblue_patterns = [
        r"\badblue\s+tank\b",
        r"\badblue[- ]tank\b",

        r"\bmit\s+adblue\b",
        r"\bmit\s+scr\b",

        r"\bscr[- ]system\b",
        r"\bscr\s+system\b",

        r"\burea[- ]tank\b",
        r"\burea\s+tank\b",

        r"\bwith\s+adblue\b",

        # Viktigt för Caraworld:
        # "2.0 l Diesel, AdBlue (Euro 6)"
        r"\badblue\s*\(",
        r"\badblue\s*\b",
    ]

    if any(
        re.search(
            pattern,
            lower,
        )
        for pattern in no_adblue_patterns
    ):

        result["adblue"] = False
        result["adblue_confidence"] = "verified"

    elif any(
        re.search(
            pattern,
            lower,
        )
        for pattern in yes_adblue_patterns
    ):

        result["adblue"] = True
        result["adblue_confidence"] = "verified"

    # --------------------------------------------------
    # SANNOLIK ADBLUE-STATUS
    # --------------------------------------------------
    #
    # Detta är INTE verifierat.
    #
    # Vi använder kombinationen:
    # basfordon + motor + årsmodell.
    #
    # Om vi inte har uttrycklig information
    # lämnas status helst okänd.
    # --------------------------------------------------

    elif (
        result["base_vehicle"] == "Fiat Ducato"
        and result["engine_size"] == 2.3
        and year
        and year >= 2019
    ):

        result["adblue"] = True
        result["adblue_confidence"] = "likely"

    return result