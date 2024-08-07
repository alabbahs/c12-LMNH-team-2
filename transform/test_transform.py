import pytest
import pandas as pd
from transform import DataProcessor
from transform import Validator


@pytest.fixture
def sample_dataframe():
    """Fixture to create sample dataframe"""
    data = {
        "last_watered": ["Mon, 01 Jan 2021 12:00:00 GMT", "Tue, 02 Feb 2021 13:30:00 GMT"],
        "scientific_name": [b"Quercus robur", b"Fagus sylvatica"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def valid_emails():
    """Fixture to provide valid emails"""
    return [
        "test@example.com",
        "user.name+tag+sorting@example.com",
        "user.name@example.co.uk",
        "user-name@domain.com",
        "user@sub.domain.com"
    ]

@pytest.fixture
def invalid_emails():
    """Fixture to provide invalid emails"""
    return [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@com",
        "username@domain..com",
        "user name@domain.com",
        "username@domain.com (Joe Smith)",
        "username@domain",
        "username@domain.c"
    ]

def test_clean_data(sample_dataframe):
    """Test the clean_data method"""

    cleaned_df = DataProcessor.clean_data(sample_dataframe)

    # Assert the 'last_watered' column is correctly transformed
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['last_watered'])
    assert cleaned_df['last_watered'].iloc[0] == pd.Timestamp("2021-01-01 12:00:00")
    assert cleaned_df['last_watered'].iloc[1] == pd.Timestamp("2021-02-02 13:30:00")

    # Assert the 'scientific_name' column is correctly transformed
    assert cleaned_df['scientific_name'].iloc[0] == "Quercus robur"
    assert cleaned_df['scientific_name'].iloc[1] == "Fagus sylvatica"

def test_is_valid_email(valid_emails, invalid_emails):
    """Test the is_valid_email method"""
    for email in valid_emails:
        assert Validator.is_valid_email(email) == True, f"Expected True for valid email: {email}"

    for email in invalid_emails:
        assert Validator.is_valid_email(email) == False, f"Expected False for invalid email: {email}"