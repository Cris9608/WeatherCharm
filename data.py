import requests
from keys import *

URL_METEORO = "https://www.meteoromania.ro/wp-json/meteoapi/v2/starea-vremii"

API_KEY_OWM = owm_key
API_OWM_GEO = "http://api.openweathermap.org/geo/1.0/direct"

API_OWM_PROG = "https://api.openweathermap.org/data/2.5/onecall"


class Data:
    def __init__(self):
        self.nume_statii = []

    def get_current_weather(self):
        # Getting hold of the current weather condition using the Meteo Romania API
        response = requests.get(URL_METEORO)
        response.raise_for_status()
        return response.json()

    def get_names(self):
        for item in self.get_current_weather()["features"]:
            nume_statie = item["properties"]["nume"].title()
            self.nume_statii.append(nume_statie)
            coord_statie = (item["geometry"]["coordinates"][0], item["geometry"]["coordinates"][1])

    def get_coord(self, name):
        '''Gets hold of latitude and longitude from the OpenWeatherMap API. Returns tuple (lat, lon).'''
        api_owm_geo_params = {
            "q": name,
            "appid": API_KEY_OWM
        }
        command = requests.get(url=API_OWM_GEO, params=api_owm_geo_params)
        data = command.json()
        coord_f = (data[0]["lat"], data[0]["lon"])
        return coord_f

    def station_names(self):
        self.get_names()
        statii_ord = sorted(self.nume_statii)
        return statii_ord


    # dict2 = {statie["properties"]["nume"].title(): (statie["geometry"]["coordinates"][0],
    #                                                 statie["geometry"]["coordinates"][1])
    #          for statie in get_current_weather()["features"]}
