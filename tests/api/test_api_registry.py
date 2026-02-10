import logging
import os
from urllib import response
import pytest
import uuid
from time import time
from utils.http_client import HttpClient
from utils.token_store import TokenStore
from datetime import datetime



logging.basicConfig(level=logging.INFO)

# Test data constants
TEST_CATALOGUE_UUID = "8965285b-5019-4349-8fcc-0f53a4389463"
TEST_RECORD_UUID = "8965285b-5019-4349-8fcc-0f53a4389463"
INVALID_UUID = "invalid-uuid-format"
NON_EXISTENT_UUID = "00000000-0000-0000-0000-000000000000"

TEST_USER = os.getenv("USERNAME_EDITOR_A")
password = os.getenv("TEST_USER_PASSWORD")  # Ensure this is set in your environment


def test_GET_API_registry_catalogue_records(client_factory):
    client = client_factory(username=TEST_USER,password=password)  # custom login
    response = client.get("/api-registry/catalogue/8965285b-5019-4349-8fcc-0f53a4389463/records")
    assert response.status_code == 200

def test_GET_API_registry_entry_points(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get("/api-registry/entryPointsUrl")
    assert response.status_code == 200
    response_data = response.json()
    # Validate response structure matches expected JSON
    assert "dashboardUrl" in response_data
    assert "en" in response_data["dashboardUrl"]
    assert "fr" in response_data["dashboardUrl"]
    
    # Validate expected URLs
    expected_en_url = "https://test.edh-cde.unclass.dfo-mpo.gc.ca/api-registry/dashboard?lang=en"
    expected_fr_url = "https://test.edh-cde.unclass.dfo-mpo.gc.ca/api-registry/dashboard?lang=fr"
    
    assert response_data["dashboardUrl"]["en"] == expected_en_url
    assert response_data["dashboardUrl"]["fr"] == expected_fr_url
    
    # Validate URLs are properly formatted
    assert response_data["dashboardUrl"]["en"].startswith("https://")
    assert response_data["dashboardUrl"]["fr"].startswith("https://")
    assert "lang=en" in response_data["dashboardUrl"]["en"]
    assert "lang=fr" in response_data["dashboardUrl"]["fr"]
    
    logging.info("test_GET_API_registry_entry_points_success passed")
def test_GET_API_registry_record_details(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get("/api-registry/records/257e64ff-0fc7-42bf-890e-7b3a248c4b92/details")
    assert response.status_code == 200
    json = response.json()
    assert json["id"] == "257e64ff-0fc7-42bf-890e-7b3a248c4b92"

 
