import logging
from urllib import response
import pytest
import uuid
from time import time
import os
from utils.http_client import HttpClient
from utils.token_store import TokenStore
from datetime import datetime

logging.basicConfig(level=logging.INFO)

OBJECT_ID = "ZG9jdW1lbnQ6cHVibGljOjE5MDM2MToweDhEREQ0RUMxMTYxREQ1RTpEYXRhX0RpY3Rpb25hcnkuaHRt"
UUID= "3a26be98-4fde-4287-acb2-838d232f7857"

TEST_USER = os.getenv("USERNAME_REVIEWER_A")
password = os.getenv("TEST_USER_PASSWORD")  # Ensure this is set in your environment

def test_GET_Metadataproperties(client_factory):
    client = client_factory(username=TEST_USER,password=password)  # custom login
    response = client.get(f"/connector/artifact/metadataProperties?objectId={OBJECT_ID}&includeCalculatedValues=true")
    assert response.status_code == 200
    logging.info("test_GET_Metadataproperties passed")

def test_GET_resources_of_record(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get(f"/connector/resources?uuid={UUID}&sort=name&approved=true&filter=%2A.%2A")
    assert response.status_code == 200
    logging.info("test_GET_resources_of_record passed")

def test_GET_validate_all_resources_content(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get(f"/validateAllResources/3a26be98-4fde-4287-acb2-838d232f7857?validationTypes=CONTENT")
    assert response.status_code == 200
    logging.info("test_GET_validate_all_resources_content passed")


def test_GET_validate_all_resources_metadata(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get(f"/validateAllResources/3a26be98-4fde-4287-acb2-838d232f7857?validationTypes=METADATA")
    assert response.status_code == 200
    logging.info("test_GET_validate_all_resources_metadata passed")

def test_GET_validate_object_content(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get(f"/connector/validate/{OBJECT_ID}/1?validationTypes=CONTENT")
    assert response.status_code == 200
    json = response.json()

def test_GET_validate_object_met(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get(f"/connector/validate/{OBJECT_ID}/1?validationTypes=CONTENT")
    assert response.status_code == 200
    json = response.json()    

def test_PATCH_resource(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.patch("/connector/artifact/metadataProperties?objectId=ZG9jdW1lbnQ6cHVibGljOjE5MDM2MToweDhEREQ0RUMxMTYxREQ1RTpEYXRhX0RpY3Rpb25hcnkuaHRt", data='''
    {
        "objectId": "ZG9jdW1lbnQ6cHVibGljOjE5MDM2MToweDhEREQ0RUMxMTYxREQ1RTpEYXRhX0RpY3Rpb25hcnkuaHRt",
        "version": "\"0x8DDD4EE28BDDD40\"",
        "name": "Data_Dictionary",
        "fileName": "Data_Dictionary.htm",
        "creationDate": "2025-02-05T16:57:27Z",
        "descriptionEnglish": "Data_Dictionary",
        "descriptionFrench": "Data_Dictionary",
        "catalogueId": "3a26be98-4fde-4287-acb2-838d232f7857",
        "status": "ACTIVE",
        "sensitivity": "UNCLASSIFIED",
        "publicationLevel": "PUBLIC",
        "topicCategories": "",
        "officialCopy": "NA",
        "maximumNumberOfVersions": 10,
        "numberOfVersions": 1,
        "publishVersionSelectionList": [
            1
        ],
        "publishVersion": 1,
        "dispositionAction": "ARCHIVE",
        "dispositionPeriodType": "YEARS",
        "dispositionPeriodCount": 999,
        "dispositionDate": "3024-02-05T16:57:27Z",
        "dispositionContactEmail": "ahmedhussain.mohammad@dfo-mpo.gc.ca",
        "archivePeriodType": "YEARS",
        "archivePeriodCount": 999,
        "archiveEndDate": "3024-02-05T16:57:27Z",
        "archiveContactEmail": "nancy.chen@dfo-mpo.gc.ca"
    }
    ''')
  #  assert response.status_code == 200