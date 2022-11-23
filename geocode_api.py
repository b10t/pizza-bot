import requests


class Geocode():
    def __init__(self, apikey) -> None:
        self.apikey = apikey

    def fetch_coordinates(self, address):
        """Получение координат по адресу."""
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url, params={
            "geocode": address,
            "apikey": self.apikey,
            "format": "json",
        })
        response.raise_for_status()
        found_places = response.json(
        )['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lat, lon
