from typing import Any


class Constants:
    # Constants go here
    LMNH_API_ENDPOINT = "https://data-eng-plants-api.herokuapp.com/plants"
    PATH_TO_DATA = "data"
    PATH_TO_LOGS = "logs"
    NUMBER_OF_PLANTS = 51
    DATA_FILENAME = "new_data.parquet"
    CLEANED_DATA_FILENAME = "clean_data.parquet"

    # No. Hours live data is stored for
    RETENTION_TIME = 24

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Can't Reassign Constant {name}")