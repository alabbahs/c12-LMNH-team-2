# Clean data and make any transformations

import sys
import os
import re
import pandas as pd
import logging
import cProfile
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG

NEW_DATA = f"{ct.PATH_TO_DATA}/{ct.DATA_FILENAME}"
CLEAN_DATA = f"{ct.PATH_TO_DATA}/{ct.CLEANED_DATA_FILENAME}"

logger = cg.setup_logging(SCRIPT_NAME, LOGGING_LEVEL)

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

        logger.info("Normalising Dates...")
        df["last_watered"] = pd.to_datetime(df["last_watered"].str.replace(" GMT", ""), format='%a, %d %b %Y %H:%M:%S')

        logger.info("Converting byte string lists to normal strings...")
        df["scientific_name"] = df["scientific_name"].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

        logger.info("Data cleaned successfully.")
        return df
    
    @staticmethod
    def save_parquet(df: pd.DataFrame, file_path: str) -> None:
        """Saves the dataframe to a Parquet file"""
        logger.info("Saving DataFrame to Parquet file at %s", file_path)
        try:
            df.to_parquet(file_path, index=False)
            logger.info("DataFrame saved to Parquet file successfully.")
        except Exception as e:
            logger.error("Failed to save DataFrame to Parquet file: %s", e)
            raise

class Validator:
    @staticmethod
    def is_valid_uk_phone_number(phone_number: str) -> bool:
        """
        Define regex patterns for different valid UK phone number
        formats and check the number fits
        """
        logger.info("Validating phone numbers..")
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
        """
        Uses regex to check whether email conforms to basic email pattern or
        if it cannot be a valid email.
        """
        logger.info("Validating emails..")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return True
        return False
    
    @staticmethod
    def validate_or_nullify(df: pd.DataFrame, column: str, validation_func) -> pd.DataFrame:
        """
        Checks the given column using the provided validation function. 
        If the validation returns False, the data is converted to NaN.
        """
        df[column] = df[column].apply(lambda x: x if validation_func(x) else np.nan)
        return df
    
def main():
    """
    Main function that ties script together, tranforming the
    data so it ready to be loaded
    """

    # Setup logging and performance tracking
    performance_logger = cg.setup_subtle_logging(SCRIPT_NAME)
    profiler = cg.start_monitor()
    logger.info("---> Logging initiated.")
    
    logger.info("---> Reading parquet..")
    df = DataProcessor.read_parquet(NEW_DATA)
    logger.info("---> Cleaning data..")
    df = DataProcessor.clean_data(df)
    logger.info("---> Validating data..")
    df = Validator.validate_or_nullify(df, 'botanist_email', Validator.is_valid_email)
    logger.info("---> Saving Parquet..")
    DataProcessor.save_parquet(df, CLEAN_DATA)

    logger.info("---> Saving Parquet..")
    cg.stop_monitor(SCRIPT_NAME, profiler, performance_logger)
    logger.info("---> Parequet saved as %s..", (SCRIPT_NAME))

    print(df)

if __name__ == "__main__":
    main()

