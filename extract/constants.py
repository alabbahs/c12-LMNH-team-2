# this file contains constants relevant to the extract folder
from typing import Any


class Constants:
    # Constants go here
    LMNH_API_ENDPOINT = "https://data-eng-plants-api.herokuapp.com/plants"
    PATH_TO_DATA = "data/"
    NUMBER_OF_PLANTS = 51
    DATA_FILENAME = "new_data_2.parquet"

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Can't Reassign Constant {name}")
