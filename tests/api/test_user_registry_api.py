import logging
import os
from urllib import response
import pytest
import uuid
from time import time
from utils.http_client import HttpClient
from utils.token_store import TokenStore
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO)

OBJECT_ID = "ZG9jdW1lbnQ6cHVibGljOjE5MDM2MToweDhEREQ0RUMxMTYxREQ1RTpEYXRhX0RpY3Rpb25hcnkuaHRt"
UUID= "3a26be98-4fde-4287-acb2-838d232f7857"
TEST_USER = os.getenv("USERNAME_REVIEWER_A")
TEST_USER_EDITOR = os.getenv("USERNAME_EDITOR_A")
password = os.getenv("TEST_USER_PASSWORD")  # Ensure this is set in your environment

reviewer_a = 'a6a4f7b0-eb62-45c4-9341-40a1a5e0baa2'
reviewer_b = '98d3e659-1405-4ddb-a4de-8703aee6cae6'
ahmed= '29077d0b-73f9-4ff3-8ce0-558c2598778d'
global today_date, week_after_date,two_weeks_after_date
today_date = datetime.now().strftime("%Y-%m-%d")
week_after_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
two_weeks_after_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

def test_GET_delegationlist(client_factory):
    client = client_factory(username=TEST_USER,password=password)  # custom login
    response = client.get(f"/user-registry/search/users/gn_reviewer_a")
    assert response.status_code == 200
    logging.info("test_GET_delegationlist passed")



def test_GET_delegation(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.get(f"/user-registry/delegations/a223843b-2f90-424f-bbb2-fed4dceb88c5")
    assert response.status_code == 200
    json = response.json()  

def test_GET_ADMIN_Roles(client_factory):
    client = client_factory(username=TEST_USER_EDITOR, password=password)  # custom login
    response = client.get(f"/user-registry/admin/clients/94fd635e-9705-4ffe-9dd3-32f1c6d286b0/roles/reviewer/users")
    assert response.status_code == 200
    
    # Parse JSON response
    json_data = response.json()
    
    # Basic structure assertions
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) > 0, "Response should contain at least one user"
    
    # Validate each user object
    for i, user in enumerate(json_data):
        # Required fields check
        required_fields = ["id", "username", "enabled", "emailVerified", "firstName", "lastName", "email"]
        for field in required_fields:
            assert field in user, f"User {i} missing required field: {field}"
        
        # ID field assertions
        assert isinstance(user["id"], str), f"User {i}: ID should be a string"
        assert len(user["id"]) > 0, f"User {i}: ID should not be empty"
        # Check if ID is UUID format
        try:
            uuid.UUID(user["id"])
        except ValueError:
            pytest.fail(f"User {i}: ID '{user['id']}' is not a valid UUID format")
        
        # Username assertions
        assert isinstance(user["username"], str), f"User {i}: Username should be a string"
        assert len(user["username"]) > 0, f"User {i}: Username should not be empty"
        assert "@" in user["username"] or user["username"].startswith("gn_"), \
            f"User {i}: Username should be email format or start with 'gn_'"
        
        # Boolean field assertions
        assert isinstance(user["enabled"], bool), f"User {i}: Enabled should be a boolean"
        assert isinstance(user["emailVerified"], bool), f"User {i}: EmailVerified should be a boolean"
        
        # Name field assertions
        assert isinstance(user["firstName"], str), f"User {i}: FirstName should be a string"
        assert isinstance(user["lastName"], str), f"User {i}: LastName should be a string"
        assert len(user["firstName"]) > 0, f"User {i}: FirstName should not be empty"
        assert len(user["lastName"]) > 0, f"User {i}: LastName should not be empty"
        
        # Email field assertions
        assert isinstance(user["email"], str), f"User {i}: Email should be a string"
        assert "@" in user["email"], f"User {i}: Email should contain '@' symbol"
        assert "." in user["email"], f"User {i}: Email should contain a domain"
        assert user["email"].count("@") == 1, f"User {i}: Email should have exactly one '@' symbol"
        assert "dfo-mpo.gc.ca" in user["email"], f"User {i}: Email should be from dfo-mpo.gc.ca domain"
    
    # Content-specific validations
    # Find specific users from your expected response
    agampodi_user = next((user for user in json_data if user["username"] == "agampodi.dezoysa@dfo-mpo.gc.ca"), None)
    api_reviewer_user = next((user for user in json_data if user["username"] == "gn_apireviewer"), None)
    
    # Validate Agampodi user if found
    if agampodi_user:
        assert agampodi_user["enabled"] == True, "Agampodi user should be enabled"
        assert agampodi_user["emailVerified"] == True, "Agampodi user email should be verified"
        assert agampodi_user["firstName"] == "Agampodi", "Agampodi firstName should match"
        assert agampodi_user["lastName"] == "De Zoysa", "Agampodi lastName should match"
        assert agampodi_user["email"] == "agampodi.dezoysa@dfo-mpo.gc.ca", "Agampodi email should match"
        logging.info("✅ Agampodi user validation passed")
    
    # Validate API Reviewer user if found
    if api_reviewer_user:
        assert api_reviewer_user["enabled"] == True, "API Reviewer should be enabled"
        assert api_reviewer_user["emailVerified"] == False, "API Reviewer email should not be verified"
        assert api_reviewer_user["firstName"] == "api", "API Reviewer firstName should be 'api'"
        assert api_reviewer_user["lastName"] == "reviewer", "API Reviewer lastName should be 'reviewer'"
        assert api_reviewer_user["email"] == "dfo.cdosedhdevtestsupport-soutiendevtestcdesdpn.mpo@dfo-mpo.gc.ca", "API Reviewer email should match"
        logging.info("✅ API Reviewer user validation passed")
    
        
def test_GET_ADMIN_Members(client_factory):
    client = client_factory(username=TEST_USER_EDITOR, password=password)  # custom login
    response = client.get(f"/user-registry/admin/groups/ddd71541-d766-40ab-96a9-56c651f82872/members")
    assert response.status_code == 200
    
    json_data = response.json()
    assert isinstance(json_data, list), "Response should be a list"
    assert len(json_data) > 0, "Response should not be empty"
    
    # Your existing validation is good - keep it
    for user in json_data:
        # ID field assertions
        assert isinstance(user["id"], str), "ID should be a string"
        assert len(user["id"]) > 0, "ID should not be empty"
        # Check if ID is UUID format
        try:
            uuid.UUID(user["id"])
        except ValueError:
            pytest.fail(f"ID '{user['id']}' is not a valid UUID format")
        
        # Username assertions
        assert isinstance(user["username"], str), "Username should be a string"
        assert len(user["username"]) > 0, "Username should not be empty"
        assert "@" in user["username"] or user["username"].startswith("gn_"), \
            "Username should be email format or start with 'gn_'"
        
        # Boolean field assertions
        assert isinstance(user["enabled"], bool), "Enabled should be a boolean"
        assert isinstance(user["emailVerified"], bool), "EmailVerified should be a boolean"
        
        # Name field assertions
        assert isinstance(user["firstName"], str), "FirstName should be a string"
        assert isinstance(user["lastName"], str), "LastName should be a string"
        assert len(user["firstName"]) > 0, "FirstName should not be empty"
        assert len(user["lastName"]) > 0, "LastName should not be empty"
        
        # Email field assertions
        assert isinstance(user["email"], str), "Email should be a string"
        assert "@" in user["email"], "Email should contain '@' symbol"
        assert "." in user["email"], "Email should contain a domain"
        assert user["email"].count("@") == 1, "Email should have exactly one '@' symbol"
    

def test_POST_delegation_create(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    data = {
        "start_date": f"{today_date} 04:00:00",
        "end_date": f"{week_after_date} 04:00:00",
        "requestor_id": "a6a4f7b0-eb62-45c4-9341-40a1a5e0baa2",
        "source_user_id": "a6a4f7b0-eb62-45c4-9341-40a1a5e0baa2",
        "target_user_id": "707edb3a-31e8-4225-94dd-26b4c3510ac9",
        "keycloak_roles": [],
        "keycloak_groups": [
            {
                "groupId": "ddd71541-d766-40ab-96a9-56c651f82872",
                "groupName": "CDOs"
            }
        ]
    }
    response = client.post("/user-registry/delegations/type/delegation", json=data)
    assert response.status_code == 201
    global delegation_id
    delegation_id = response.json().get("id")
    assert delegation_id is not None

def test_PATCH_delegation_modify_date(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.patch(
        f"/user-registry/delegations/{delegation_id}",
        data=f'{{"end_date": "{two_weeks_after_date} 04:00:00"}}'
    )
    assert response.status_code == 200
    logging.info("test_PATCH_delegation passed")


def test_PATCH_delegation_cancel(client_factory):
    client = client_factory(username=TEST_USER, password=password)  # custom login
    response = client.patch(f"/user-registry/delegations/{delegation_id}/cancel", data='''')    ''')
    assert response.status_code == 200
    logging.info("test_PATCH_delegation passed")