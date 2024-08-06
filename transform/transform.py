# Clean data and make any transformations

import sys
import os
import re
import pandas as pd
import logging
import cProfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG

NEW_DATA = f"{ct.PATH_TO_DATA}/{ct.DATA_FILENAME}"
CLEAN_DATA = f"{ct.PATH_TO_DATA}/{ct.CLEANED_DATA_FILENAME}"
GENERIC_LOG = f"{ct.PATH_TO_LOGS}/{SCRIPT_NAME}"
PERFORMANCE_LOG = f"{ct.PATH_TO_LOGS}/{SCRIPT_NAME}_performance"

logger = cg.setup_logging(GENERIC_LOG, LOGGING_LEVEL)


class DataProcessor:
    @staticmethod
    def read_parquet(file_path: str) -> pd.DataFrame:
        """Reads a Parquet file and returns a dataframe"""
        logger.info("Reading Parquet file from %s", file_path)
        try:
            df = pd.read_parquet(file_path)
            logger.info("Parquet file read successfully.")
            return df
        except Exception as e:
            logger.error("Failed to read Parquet file: %s", e)
            raise
   
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Placeholder for data cleaning and transformation logic"""
        logger.info("Cleaning data...")
        # Add any data cleaning logic here
        logger.info("Data cleaned successfully.")
        return df

class Validator:
    @staticmethod
    def is_valid_uk_phone_number(phone_number: str) -> bool:
        """Define regex patterns for different valid UK phone number
        formats and check the number fits"""
        patterns = [
            r'^(?:\+44|0)7\d{9}$',                 # Mobile numbers, e.g., +447123456789 or 07123456789
            r'^(?:\+44|0)1\d{3}\s?\d{6}$',         # National numbers, e.g., +441234567890 or 01234567890
            r'^(?:\+44|0)1\d{2}\s?\d{3}\s?\d{4}$', # National numbers, e.g., +44123 456 7890 or 0123 456 7890
            r'^(?:\+44|0)2\d{3}\s?\d{6}$',         # London numbers, e.g., +442012345678 or 02012345678
            r'^(?:\+44|0)2\d{2}\s?\d{3}\s?\d{4}$', # London numbers, e.g., +4420 123 45678 or 020 123 45678
            r'^(?:\+44|0)800\s?\d{3}\s?\d{4}$',    # Freephone numbers, e.g., +44800 123 4567 or 0800 123 4567
        ]

        for pattern in patterns:
            if re.match(pattern, phone_number):
                return True
        return False

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Uses regex to check whether email conforms to basic email pattern or
        if it cannot be a valid email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return True
        return False
    
def main():
    """Main function that ties script together, tranforming the
    data so it ready to be loaded"""

    # Setup logging and performance tracking
    performance_logger = cg.setup_subtle_logging(PERFORMANCE_LOG)
    profiler = cg.start_monitor()
    logger.info("---> Logging initiated.")
    
    df = DataProcessor.read_parquet(NEW_DATA)
    df = DataProcessor.clean_data(df)

    print(df)

