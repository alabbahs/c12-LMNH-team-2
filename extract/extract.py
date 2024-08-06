from flask import Flask, jsonify
import requests
from constants import Constants as c
from pprint import pprint

# write an extract class


class Extract:

    def __init__(self, api_endpoint: str) -> None:
        self._endpoint = api_endpoint

        pass

    # TODO write a function that gets information on a single plant
    def get_plant(self, plant_id: int) -> dict:
        """
        Given an integer as a plant id, return the dictionary associated with
        that plant id endpoint
        """

        response = requests.get(f"{self._endpoint}/{plant_id}")
        if response.status_code == 200:
            return response.json()
        pass

    # TODO write a function that flattens composite plant information

    def flatten_plant_information(self, plant_info: dict) -> dict:
        """
        Returns the plant information in a fully flattened format
        """
        if type(plant_info) != dict:
            raise TypeError("Plant info needs to be a dictionary")

        location_information = self.flatten_location_information(plant_info)
        botanist_information = self.flatten_botanist_information(plant_info)

    def flatten_botanist_information(self, plant_info: dict) -> dict:
        """
        Flattens the botanist field
        """
        if type(plant_info) != dict:
            raise TypeError("Plant info needs to be a dictionary")

        botanist_fields = plant_info.get('botanist')

        if not botanist_fields:
            raise ValueError("The botanist field is empty?!?")

        email = botanist_fields.get('email')
        name = botanist_fields.get('name')
        phone = botanist_fields.get('phone')

        return {"botanist_name": name,
                "botanist_email": email,
                "botanist_phone": phone}

    def flatten_location_information(self, plant_info: dict) -> dict:
        """
        Flattens the location field
        """

        if type(plant_info) != dict:
            raise TypeError("Plant info needs to be a dictionary")

        location_information = plant_info.get('origin_location')

        if len(location_information) < 5:
            raise ValueError("Missing plant origin location information")

        latitude = location_information[0]
        longitude = location_information[1]
        city_name = location_information[2]
        country_code = location_information[3]
        region = location_information[4]

        return {"origin_location_latitude": latitude,
                "origin_location_longitude": longitude,
                "origin_location_city_name": city_name,
                "origin_location_country_code": country_code,
                "origin_location_region": region}

    # TODO write a function that collates all the plant info into a dataframe


if __name__ == "__main__":
    plant_api = Extract(c.LMNH_API_ENDPOINT)
    pprint(plant_api.get_plant(3))
