from flask import Flask, jsonify
import requests
import pandas as pd
from constants import Constants as c
from pprint import pprint

# write an extract class


class Extract:

    def __init__(self, api_endpoint: str) -> None:
        self._endpoint = api_endpoint

        pass

    def get_plant(self, plant_id: int) -> dict:
        """
        Given an integer as a plant id, return the dictionary associated with
        that plant id endpoint
        """

        response = requests.get(f"{self._endpoint}/{plant_id}")
        if response.status_code == 200:
            return response.json()
        pass

    def generate_plant_dataframe(self) -> None:
        """
        Generates a dataframe of the 51 plant id's in 
        the LMNH
        """

        all_plant_data = []

        for i in range(c.NUMBER_OF_PLANTS):
            plant_data = self.get_plant(i)

            if plant_data == None:
                continue

            if 'error' in plant_data.keys():
                continue

            try:
                all_plant_data.append(
                    self.flatten_plant_information(plant_data))
            except Exception:
                continue

        all_plant_dataframe = pd.DataFrame(all_plant_data)
        all_plant_dataframe.to_parquet(f"{c.PATH_TO_DATA}{c.DATA_FILENAME}")

    def flatten_plant_information(self, plant_info: dict) -> dict:
        """
        Returns the plant information in a fully flattened format
        """
        if type(plant_info) != dict:
            raise TypeError("Plant info needs to be a dictionary")

        location_information = self.flatten_location_information(plant_info)
        botanist_information = self.flatten_botanist_information(plant_info)
        flattened_plant_information = plant_info.copy()
        del flattened_plant_information['botanist']
        del flattened_plant_information['origin_location']

        if 'images' in plant_info.keys():
            del flattened_plant_information['images']

        flattened_plant_information.update(location_information)
        flattened_plant_information.update(botanist_information)

        return flattened_plant_information

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


if __name__ == "__main__":
    plant_api = Extract(c.LMNH_API_ENDPOINT)
    plant_api.generate_plant_dataframe()
