
import pytest
from constants import Constants as c
from extract import Extract


def test_flatten_botanist_basic_test_1():
    lmnh = Extract(c.LMNH_API_ENDPOINT)

    assert lmnh.flatten_botanist_information({'botanist': {'email': 'eliza.andrews@lnhm.co.uk',
                                                           'name': 'Eliza Andrews',
                                                           'phone': '(846)669-6651x75948'},
                                              'last_watered': 'Mon, 05 Aug 2024 14:50:16 GMT',
                                              'name': 'Rafflesia arnoldii',
                                              'origin_location': ['-19.32556',
                                                                  '-41.25528',
                                                                  'Resplendor',
                                                                  'BR',
                                                                  'America/Sao_Paulo'],
                                              'plant_id': 3,
                                              'recording_taken': '2024-08-05 16:30:30',
                                              'soil_moisture': 94.22231965898175,
                                              'temperature': 10.014324553245878}) == {'botanist_email': 'eliza.andrews@lnhm.co.uk',
                                                                                      'botanist_name': 'Eliza Andrews',
                                                                                      'botanist_phone': '(846)669-6651x75948'}


def test_flatten_botanist_raises_error():
    with pytest.raises(TypeError):
        lmnh = Extract(c.LMNH_API_ENDPOINT)
        lmnh.flatten_botanist_information("Rigmarole")


def test_flatten_location_information_basic_test_1():
    lmnh = Extract(c.LMNH_API_ENDPOINT)

    assert lmnh.flatten_location_information({'botanist': {'email': 'eliza.andrews@lnhm.co.uk',
                                                           'name': 'Eliza Andrews',
                                                           'phone': '(846)669-6651x75948'},
                                              'last_watered': 'Mon, 05 Aug 2024 14:50:16 GMT',
                                              'name': 'Rafflesia arnoldii',
                                              'origin_location': ['-19.32556',
                                                                  '-41.25528',
                                                                  'Resplendor',
                                                                  'BR',
                                                                  'America/Sao_Paulo'],
                                              'plant_id': 3,
                                              'recording_taken': '2024-08-05 16:30:30',
                                              'soil_moisture': 94.22231965898175,
                                              'temperature': 10.014324553245878}) == {"origin_location_latitude": '-19.32556',
                                                                                      "origin_location_longitude": '-41.25528',
                                                                                      "origin_location_city_name": 'Resplendor',
                                                                                      "origin_location_country_code": 'BR',
                                                                                      "origin_location_region": 'America/Sao_Paulo'}


def test_flatten_location_information_raises_error():
    with pytest.raises(TypeError):
        lmnh = Extract(c.LMNH_API_ENDPOINT)
        lmnh.flatten_location_information("Rigmarole")
