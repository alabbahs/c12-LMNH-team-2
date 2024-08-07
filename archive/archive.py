import sys
import os
import pyodbc
import pandas as pd
import boto3
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
from io import BytesIO

sys.path.insert(0, os.path.abspath\
                (os.path.join(os.path.dirname(__file__), '..')))
import config as cg
from constants import Constants as ct

SCRIPT_NAME = (os.path.basename(__file__)).split(".")[0]
LOGGING_LEVEL = logging.DEBUG

RETENTION_TIME = ct.RETENTION_TIME
ARCHIVED_DATA = ct.ARCHIVED_DATA
S3_BUCKET = ct.S3_BUCKET
DELETE_OLD = False # Set to False when debugging

CLEAN_DATA = f"{ct.PATH_TO_DATA}/{ct.CLEANED_DATA_FILENAME}"

load_dotenv('.env')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_NAME=os.getenv('DB_NAME')

AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_REGION=os.getenv('AWS_REGION')

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
                      logger: logging.Logger = logger) -> pyodbc.Connection:
        """
        Connects to the Microsoft SQL Server database.
        """

        logger.info("Attempting to connect using the\
                    following credentials:")
        logger.info("To Host: `%s`", db_host)
        logger.info("On Port: `%s`", db_port)
        logger.info("As user: `%s`", db_user)
        logger.info("With password: `%s`", db_password)
        logger.info("Database name: `%s`", db_name)
        
        try:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};\
                SERVER={db_host},{db_port}\
                    DATABASE={db_name};\
                        UID={db_user};\
                            PWD={db_password}"
            connection = pyodbc.connect(connection_string)
            logger.info("Database connection established successfully.")
            return connection
        except Exception as e:
            logger.error("Failed to connect to the database: %s", e)
            raise

    @staticmethod
    def get_cutoff_time(retention_time: int = RETENTION_TIME,
                        logger: logging.Logger = logger) -> datetime:
        """
        Gets the last datetime that is within the data retention window.
        
        If the retention time is 1, and the time is 1500, it will return
        1400. Times before 1400 are outside the intended retention window.
        """

        logger.info(f"Retention time set to {retention_time} hours")
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=retention_time)
        logger.info(f"Setting cutoff threshold for {cutoff_time}.")
        return cutoff_time

    @staticmethod
    def extract_and_delete(cut_off_time: datetime,
                           connection: pyodbc.Connection,
                           delete: bool = DELETE_OLD,
                           logger: logging.Logger = logger) -> pd.DataFrame:
        """
        Gets the rows with times/dates beyond the cutoff limit
        from the live database.

        Returns them as a pandas DataFrame to preserve them, but deletes
        them from the  actual database if `delete` is True.
        """

        cursor = connection.cursor()

        logger.info(f"Only retaining data from {cut_off_time}"
                    f" to {datetime.now()}")

        select_query = """
        SELECT *
        FROM plants.beta.reading
        WHERE recording_taken < ? OR recording_taken > ?;
        """
        delete_query = """
        DELETE FROM plants.beta.reading
        WHERE recording_taken < ? OR recording_taken > ?;
        """
        
        cursor.execute(select_query, cut_off_time, datetime.now())
        results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame.from_records(results, columns=columns)
        
        logger.info(f"Number of rows to delete: {len(df)}")
        
        if delete:
            cursor.execute(delete_query, cut_off_time, datetime.now())
            connection.commit()
            logger.info("Extracted data deleted from database.")
        else:
            logger.info("Extracted data not deleted from database.")
       
        cursor.close()
        return df

class DataArchiver:
    """
    This class handles the archiving of data removed from the live database
    and archives it in an S3 Bucket.
    """

    @staticmethod
    def get_client(access_key: str = AWS_ACCESS_KEY,
                   secret_key: str = AWS_SECRET_KEY,
                   region: str = AWS_REGION,
                   logger: logging.Logger = logger) -> boto3.client:
        """
        Gets the boto3 client so that s3 bucket can be accessed
        """

        logger.info("Fetching boto3 client...")

        # Assume `cg.obscure` is a function to obscure sensitive info
        # logger.info("AWS access key: `%s`", cg.obscure(access_key))
        # logger.info("AWS secret key: `%s`", cg.obscure(secret_key))

        try:
            client = boto3.client('s3',
                                  access_key,
                                  secret_key,
                                  region)
            logger.info("Retrieved client successfully.")
            logger.debug(f"Client: {client}")

        except Exception as e:
            logger.error("Failed to get client!")
            logger.error(f"{e}")
            return None  # Return None if client creation fails

        return client

    @staticmethod
    def get_archived_data(client: boto3.client,
                          archive: str = ARCHIVED_DATA,
                          bucket: str = S3_BUCKET,
                          logger: logging.Logger = logger) -> pd.DataFrame:
        """
        Get archived data from an S3 bucket, returns as pandas DataFrame.
        """

        logger.info("Getting archived data from bucket...")

        try:
            obj_response = client.get_object(Bucket=bucket, Key=archive)
            
            data = obj_response['Body'].read()
            df = pd.read_parquet(BytesIO(data))

            logger.info(f"Successfully retrieved data from {archive}")

            return df

        except client.exceptions.NoSuchKey:
            logger.warning(f"File {archive} not found in bucket {bucket}.")
            logger.warning("(! ignore if bucket is supposed to be empty !)")
            return pd.DataFrame() 

        except Exception as e:
            logger.error(f"Error retrieving data from bucket: {e}")
            return pd.DataFrame()

    @staticmethod
    def merge_data(existing_data: pd.DataFrame, 
                new_data: pd.DataFrame, 
                logger: logging.Logger = logger) -> pd.DataFrame:
        """
        Merge existing data with new data while preventing duplicates.
        """
        
        logger.info("Merging existing data (if any) with new data...")

        if existing_data.empty:
            merged_df = new_data
            logger.info("Existing data is empty, returning new data as merged result.")
        else:
            check_for_duplicates_in = ['plant_id', 'recording_taken']
            merged_df = pd.concat([existing_data, new_data])\
                .drop_duplicates(subset=check_for_duplicates_in)
        
        return merged_df
        
    @staticmethod
    def save_data_to_s3(client: boto3.client, 
                        data: pd.DataFrame,
                        file_name: str = ARCHIVED_DATA,
                        bucket: str = S3_BUCKET,
                        logger: logging.Logger = logger) -> None:
        """
        Save data to the S3 bucket.
        """
        
        buffer = BytesIO()
        data.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        try:
            client.put_object(Bucket=bucket, Key=file_name, Body=buffer)
            logger.info("Merged data successfully saved to S3.")
        except Exception as e:
            logger.error(f"Error saving merged data to S3: {e}")
    
def main():

    # Setup logging and performance tracking
    performance_logger = cg.setup_subtle_logging(SCRIPT_NAME)
    profiler = cg.start_monitor()
    logger.info("---> Logging initiated.")

    # Get connection
    logger.info("---> Connecting to the database..")
    connection = DataTrimmer.connect_to_db()
    logger.info("---> Getting S3 Bucket client..")
    client = DataArchiver.get_client()

    # Extract old data that is no longer needed in live database
    logger.info("---> Assessing which time-window to keep..")
    cut_off_time = DataTrimmer.get_cutoff_time()
    logger.info("---> Extracting old data from database..")
    to_be_archived = DataTrimmer.extract_and_delete(cut_off_time, connection)

    # Merge the existing archive with the data just taken from the database
    logger.info("---> Fetching any previously archived data..")
    previously_archived = DataArchiver.get_archived_data(client)
    logger.info("---> Merging archival data..")
    joined_df = DataArchiver.merge_data(previously_archived, to_be_archived)
    logger.info("---> Saving updated archive to bucket..")
    DataArchiver.save_data_to_s3(client, joined_df)

    # Winds down, stores performance log.
    logger.info("---> Operation completed. Stopping performance monitor.")
    cg.stop_monitor(SCRIPT_NAME, profiler, performance_logger)
    logger.info("---> Data inserted and process"
                "completed for %s.", SCRIPT_NAME)


if __name__ == "__main__":
    main()