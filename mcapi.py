import requests

version = "1.20"

url = f"https://raw.githubusercontent.com/PrismarineJS/minecraft-data/master/data/pc/{version}/entities.json"


def get_data() -> list[dict]:
    return requests.get(url).json()
