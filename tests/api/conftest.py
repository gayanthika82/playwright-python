import pytest
import logging
from utils.http_client import HttpClient
from utils.token_store import TokenStore
from dotenv import load_dotenv
import os



load_dotenv()


load_dotenv(".env.test")
BASE_URL = os.getenv("API_BASE_URL")  # Replace with your actual base URL

@pytest.fixture(scope="session")
def client_factory():
    def _create_client(username="test", password="pass",header=None):
        http = HttpClient(BASE_URL)
        try:
            form_data = {
                
                'client_id': "qa-cli",
                'username': username,
                'password': password,
                'scope': "openid email profile",
                'grant_type': 'password'
            }
            login_response = http.post("/auth/realms/edh/protocol/openid-connect/token", data=form_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            print(f"Response status: {login_response.status_code}")
            print(f"Response body: {login_response.text}")
            print(f"Request Headers: {dict(login_response.headers)}")
            logging.info(f"Login response status: {login_response.status_code}")
            #logging.info(f"Login response body: {login_response.text}")
            
            if login_response.status_code == 200:
                response_data = login_response.json()
                token = response_data.get("access_token")               
                logging.info(f"Extracted token (first 50 chars): {token[:50] if token else 'None'}...")
            else:
                token = None
            if token:
                TokenStore.set_token(token)
                http.set_header("Authorization", f"Bearer {token}")
                http.set_header("Content-Type", "application/json")
                logging.info(f"Token set for user: {username}")
            else:
                logging.info("Login succeeded but no token returned.")
        except Exception as e:
            logging.info(f"Login failed: {e}")
        return http

    return _create_client

