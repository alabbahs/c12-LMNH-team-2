import sys
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import logging
import cProfile
from pprint import pprint

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG
NEW_DATA = f"{ct.PATH_TO_DATA}/{ct.DATA_FILENAME}"

load_dotenv('.env')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_NAME=os.getenv('DB_NAME')
logger = cg.setup_logging(SCRIPT_NAME, LOGGING_LEVEL)

# Write an extract class
class Extract:
    def __init__(self, api_endpoint: str) -> None:
        self._endpoint = api_endpoint

    def get_plant(self, plant_id: int) -> dict:
        """
        Given an integer as a plant id, return the dictionary associated with
        that plant id endpoint
        """
        response = requests.get(f"{self._endpoint}/{plant_id}")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get data for plant ID {plant_id}. Status code: {response.status_code}")
            return None
        
    def generate_plant_dataframe(self) -> None:
        """
        Generates a dataframe of the 51 plant id's in
        the LMNH
        """
        all_plant_data = []
        for i in range(ct.NUMBER_OF_PLANTS):
            plant_data = self.get_plant(i)
            if plant_data is None:
                logger.warning(f"Skipping plant ID {i} due to missing data.")
                continue
            if 'error' in plant_data.keys():
                logger.warning(f"Error in plant data for plant ID {i}: {plant_data['error']}")
                continue
            try:
                all_plant_data.append(self.flatten_plant_information(plant_data))
            except Exception as e:
                logger.exception(f"Exception while flattening plant data for plant ID {i}: {e}")
                continue
        all_plant_dataframe = pd.DataFrame(all_plant_data)
        try:
            all_plant_dataframe.to_parquet(NEW_DATA)
            logger.info(f"Successfully saved plant dataframe to {NEW_DATA}")
        except Exception as e:
            logger.exception(f"Exception while saving dataframe to parquet: {e}")

    def flatten_plant_information(self, plant_info: dict) -> dict:
        """
        Returns the plant information in a fully flattened format
        """
        if not isinstance(plant_info, dict):
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
        if not isinstance(plant_info, dict):
            raise TypeError("Plant info needs to be a dictionary")
        botanist_fields = plant_info.get('botanist')
        if not botanist_fields:
            raise ValueError("The botanist field is empty?!?")
        email = botanist_fields.get('email')
        name = botanist_fields.get('name')
        phone = botanist_fields.get('phone')
        return {"botanist_name": name, "botanist_email": email, "botanist_phone": phone}
    
    def flatten_location_information(self, plant_info: dict) -> dict:
        """
        Flattens the location field
        """
        if not isinstance(plant_info, dict):
            raise TypeError("Plant info needs to be a dictionary")
        location_information = plant_info.get('origin_location')
        if len(location_information) < 5:
            raise ValueError("Missing plant origin location information")
        latitude = location_information[0]
        longitude = location_information[1]
        city_name = location_information[2]
        country_code = location_information[3]
        region = location_information[4]
        return {
            "origin_location_latitude": latitude,
            "origin_location_longitude": longitude,
            "origin_location_city_name": city_name,
            "origin_location_country_code": country_code,
            "origin_location_region": region,
        }
def main_extract():
    """
    Main function to initialize the extraction and transformation
    of plant data into a dataframe and save it as parquet.
    """
    performance_logger = cg.setup_subtle_logging(SCRIPT_NAME)
    profiler = cg.start_monitor()
    logger.info("---> Logging initiated.")

    logger.info("---> Initializing Extract class..")
    plant_api = Extract(ct.LMNH_API_ENDPOINT)

    logger.info("---> Generating plant dataframe..")
    plant_api.generate_plant_dataframe()

    logger.info("---> Operation completed. Stopping performance monitor.")
    cg.stop_monitor(SCRIPT_NAME, profiler, performance_logger)

    logger.info("---> Dataframe generation and save completed for %s.", SCRIPT_NAME)


if __name__ == "__main__":
    main_extract()