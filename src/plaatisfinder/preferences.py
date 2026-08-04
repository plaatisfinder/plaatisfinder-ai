def get_preferences():

    return {

        # Märken du är intresserad av
        "brands": [
            "Adria",
            "Pössl",
            "Globecar",
            "Weinsberg",
            "Knaus",
        ],

        # Lämna tom = alla modeller från ovanstående märken.
        # AI kommer senare att ge extra poäng till favoritmodeller.
        "models": [],

        # Pris
        "max_price": 45000,

        # Årsmodell
        "min_year": 2015,

        # Körsträcka
        "max_mileage": 100000,

        # dealer / private / any
        "seller_type": "dealer",

        # Länder
        "countries": [
            "FI",
            "DE",
        ],
    }