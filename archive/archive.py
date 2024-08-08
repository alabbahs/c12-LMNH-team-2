import sys
import os
import pyodbc
import pandas as pd
import boto3
from dotenv import load_dotenv

import logging
import cProfile
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG

RETENTION_TIME = ct.RETENTION_TIME

CLEAN_DATA = f"{ct.PATH_TO_DATA}/{ct.CLEANED_DATA_FILENAME}"

load_dotenv('.env')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_NAME=os.getenv('DB_NAME')

logger = cg.setup_logging(SCRIPT_NAME, LOGGING_LEVEL)

class DataTrimmer:
    """
    Finds database data that is outside of a retention window (e.g. 24hrs).

    Removes it from a database. Returns removed data as a dataframe.
    """

    @staticmethod
    def connect_to_db(db_host: str = DB_HOST,
                      db_port: str = DB_PORT,
                      db_user: str = DB_USER,
                      db_password: str = DB_PASSWORD,
                      db_name: str = DB_NAME,
                      logger: logging.Logger=logger)\
                                                        -> pyodbc.Connection:
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
    

    @static_method
    def get_cutoff_time(retention_time: int = RETENTION_TIME,
                        logger: logging.Logger=logger)\
                                                            -> datetime:
        """
        Gets the last datetime that is within the data retention window.
        
        If the retention time is 1, and the time is 1500, it will return
        1400. Times before 1400 are outside the intended retention window.
        """
        logger.info(f"Retention time set to {retention_time}Hrs")
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=retention_time)
        logger.info(f"Setting cutoff threshold for {cutoff_time}.")
        return cutoff_time

    @static_method
    def extract_and_delete(cut_off_time: datetime,
                           connection: any,
                           logger: logging.Logger=logger)\
                                                            -> pd.DataFrame:
        """
        Gets the times/dates beyond the cutoff limit from the live database.

        Returns them as a pandas to preserve them, but deletes them from the 
        actual database.
        """

        cursor = connection.cursor()
        logger.info(f"Only retaining data from {cut_off_time}\
                    -> {datetime.datetime.now()}")

        select_query = """
        SELECT *
        FROM data_table
        WHERE date_column < ? OR date_column > ?;
        """
        cursor.execute(select_query, cut_off_time, datetime.datetime.now())
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame.from_records(results, columns=columns)
        
        logger.info(f"Number of rows to delete: {len(df)}")
        
        delete_query = """
        DELETE FROM data_table
        WHERE date_column < ? OR date_column > ?;
        """
        cursor.execute(delete_query, cut_off_time, datetime.datetime.now())
        connection.commit()
        logger.info(f"Old data deleted")
        cursor.close()
        
        return df

class DataArchiver:
    """
    This class handles the archiving of data removed from the live database
    and archives it in an S3 Bucket.
    """

    @staticmethod
    def get_client(access_key: str,
                secret_key: str,
                region: str,
                logger: logging.Logger=logger)\
                                               -> boto3.client:
        logger.info("Fetching boto3 client...")

        try:
            client = boto3.client('s3',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,
                                region_name=region
                                )
            logger.info("Retrieved client successfully.")
            logger.debug(f"Client: {client}")

        except Exception as e:
            logger.error("Failed to get client!")
            logger.error(f"{e}")

        return client


if __name__ == "__main__":
    main()