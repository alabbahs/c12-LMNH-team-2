from typing import Any


class Constants:
    # Constants go here
    LMNH_API_ENDPOINT = "https://data-eng-plants-api.herokuapp.com/plants"
    PATH_TO_DATA = "/tmp"
    PATH_TO_LOGS = "/tmp"
    NUMBER_OF_PLANTS = 51
    DATA_FILENAME = "new_data.parquet"
    CLEANED_DATA_FILENAME = "clean_data.parquet"

    # No. Hours live data is stored for
    RETENTION_TIME = 1
    #Name of S3 Bucket
    S3_BUCKET = "c12-lmnh-plants-team2-bucket"
    # Parquet name of historic data on s3
    ARCHIVED_DATA = "archived_data.parquet"



    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Can't Reassign Constant {name}")