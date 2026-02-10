import logging
import os
from time import time

logging.basicConfig(level=logging.INFO)


TEST_USER = os.getenv("USERNAME_REVIEWER_A")
password = os.getenv("TEST_USER_PASSWORD")  # Ensure this is set in your environment

def test_GET_publishing_apis_publishableChannels(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get("/publishing/channel/publishableChannels/c3e4ba88-825e-4ebb-a302-2da0f0a9fa15/details?checkPermissionsFirst=false")
    assert response.status_code == 200

def test_GET_publishing_apis_validation(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    channelname='OI'
    response = client.get(f"/publishing/channel/validation/c3e4ba88-825e-4ebb-a302-2da0f0a9fa15?channel={channelname}")
    assert response.status_code == 200


def test_GET_publishing_apis_data_channel(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login

    response = client.get("/publishing/data/channel")
    assert response.status_code == 200


def test_GET_publishing_apis_entryPointsUrl(client_factory):
    client = client_factory(username=TEST_USER, password="password")  # custom login
    response = client.get("/publishing/entryPointsUrl")
    assert response.status_code == 200

def test_POST_publishing_apis_publication_current(client_factory):
    client = client_factory(username=TEST_USER, password="password")  # custom login
    response = client.post("/publishing/publication/current", data='["c3e4ba88-825e-4ebb-a302-2da0f0a9fa15"]')
  #  assert response.status_code == 200


def test_GET_publishing_apis_publication_current_uuid(client_factory):
    client = client_factory(username=TEST_USER, password="password")  # custom login
    response = client.get("/publishing/publication/current/c3e4ba88-825e-4ebb-a302-2da0f0a9fa15")
    assert response.status_code == 200

def test_GET_publishing_apis_publication_history_uuid(client_factory):
    client = client_factory(username=TEST_USER, password="password")  # custom login
    response = client.get("/publishing/publication/history/c3e4ba88-825e-4ebb-a302-2da0f0a9fa15")
    assert response.status_code == 200

def test_GET_publishing_apis_publication_inProgress_uuid(client_factory):
    client = client_factory(username=TEST_USER, password="password")  # custom login       
    response = client.get("/publishing/publication/inProgress/c3e4ba88-825e-4ebb-a302-2da0f0a9fa15?channel=FGP")
    assert response.status_code == 200


def test_GET_publishing_apis_publication_platforms(client_factory):
    client = client_factory(username=TEST_USER, password="password")  # custom login
    response = client.get("/publishing/publication/platforms/c3e4ba88-825e-4ebb-a302-2da0f0a9fa15")
    assert response.status_code == 200