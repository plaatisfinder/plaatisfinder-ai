import json


def load_filters():
    with open("config/search_filters.json", encoding="utf-8") as f:
        return json.load(f)