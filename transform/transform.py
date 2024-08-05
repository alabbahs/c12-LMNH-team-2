# Clean data and make any transformations

import sys
import os
import re
import pandas as pd
import pickle

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config as cg
import constants as cs



def open_pickled_df(file_path: str) -> pd.DataFrame:
    """Takes a path to a pickled dtaframe and opens it, returning the
    dataframe"""
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        return data


def is_valid_uk_phone_number(phone_number):
    """Define regex patterns for different valid UK phone number formats
    and check the number fits"""
    patterns = [
        r'^(?:\+44|0)7\d{9}$',                       # Mobile numbers, e.g., +447123456789 or 07123456789
        r'^(?:\+44|0)1\d{3}\s?\d{6}$',                # National numbers, e.g., +441234567890 or 01234567890
        r'^(?:\+44|0)1\d{2}\s?\d{3}\s?\d{4}$',        # National numbers, e.g., +44123 456 7890 or 0123 456 7890
        r'^(?:\+44|0)2\d{3}\s?\d{6}$',                # London numbers, e.g., +442012345678 or 02012345678
        r'^(?:\+44|0)2\d{2}\s?\d{3}\s?\d{4}$',        # London numbers, e.g., +4420 123 45678 or 020 123 45678
        r'^(?:\+44|0)800\s?\d{3}\s?\d{4}$',           # Freephone numbers, e.g., +44800 123 4567 or 0800 123 4567
    ]

    for pattern in patterns:
        if re.match(pattern, phone_number):
            return True
    return False

def is_valid_email(email):
    """Uses regex to check whether email conforms to basic email 
    pattern or if it cannot be a valid email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False