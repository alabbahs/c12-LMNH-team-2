import sys
import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

import logging
import cProfile
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG

CLEAN_DATA = f"{ct.PATH_TO_DATA}/{ct.CLEANED_DATA_FILENAME}"

load_dotenv('.env')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_NAME=os.getenv('DB_NAME')

logger = cg.setup_logging(SCRIPT_NAME, LOGGING_LEVEL)

class DataLoader:

    @staticmethod
    def connect_to_db(db_host: str = DB_HOST, db_port: str = DB_PORT,
                      db_user: str = DB_USER, db_password: str = DB_PASSWORD,
                      db_name: str = DB_NAME):
        """Connects to the Microsoft SQL Server database"""

        logger.info("Attempting to connectng using the following credentials:")
        logger.info("To Host: `%s`", db_host)
        logger.info("On Port: `%s`", db_port)
        logger.info("As user: `%s`", db_user)
        logger.info("With password: `%s`", cg.obscure(db_password))
        logger.info("Database name: `%s`", db_name)
        
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host},{db_port};DATABASE={db_name};UID={db_user};PWD={db_password}"
            connection = pyodbc.connect(connection_string)
            logger.info("Database connection established successfully.")
            return connection
        except Exception as e:
            logger.error("Failed to connect to the database: %s", e)
            raise


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
    def insert_data_from_df(df: pd.DataFrame, connection):
        """Inserts data from a DataFrame into the database"""
        cursor = connection.cursor()
        try:
            for _, row in df.iterrows():
                query = """
                INSERT INTO beta.reading (last_watered, soil_moisture, temperature, plant_id, recording_taken)
                VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, (
                    row['last_watered'],
                    row['soil_moisture'],
                    row['temperature'],
                    row['plant_id'],
                    row['recording_taken']
                ))
            connection.commit()
            logger.info("Data inserted successfully.")
        except Exception as e:
            logger.error("Failed to insert data into the database: %s", e)
            connection.rollback()
            raise
        finally:
            cursor.close()


def main():
    """
    Main function that reads data from parquet and inserts it into the database.
    """

    # Setup logging and performance tracking
    performance_logger = cg.setup_subtle_logging(SCRIPT_NAME)
    profiler = cg.start_monitor()
    logger.info("---> Logging initiated.")
    
    # Get connection
    logger.info("---> Connecting to the database..")
    connection = DataLoader.connect_to_db()
    
    # Get dataframe from parquet
    logger.info("---> Reading parquet..")
    df = DataLoader.read_parquet(CLEAN_DATA)
    
    # Opens cursor, loads data, closes cursor.
    logger.info("---> Inserting data into the database..")
    DataLoader.insert_data_from_df(df, connection)
    
    # Winds down, stores performance log.
    logger.info("---> Operation completed. Stopping performance monitor.")
    cg.stop_monitor(SCRIPT_NAME, profiler, performance_logger)
    logger.info("---> Data inserted and process completed for %s.", SCRIPT_NAME)

    print(df)

if __name__ == "__main__":
    main()