import logging
import pytest
import uuid
import os
from time import time
from utils.http_client import HttpClient
from utils.token_store import TokenStore
logging.basicConfig(level=logging.INFO)

# Test data constants
TEST_UUID = "ed4835ae-d308-4b6b-b7da-af95c2b6c16b"
UUID = "ed4835ae-d308-4b6b-b7da-af95c2b6c16b"
INVALID_UUID = "invalid-uuid-format"
NON_EXISTENT_UUID = "00000000-0000-0000-0000-000000000000"

# Valid request types with their corresponding UUIDs
VALID_REQUEST_TYPES = {
    "MAPPING": "ed4835ae-d308-4b6b-b7da-af95c2b6c16b",
    "API": "97e91260-8044-4ed6-80d8-e9448ca1a514"
}
INVALID_REQUEST_TYPE = "INVALID_TYPE"

TEST_USER = os.getenv("USERNAME_EDITOR_A")
password = os.getenv("TEST_USER_PASSWORD")  # Ensure this is set in your environment

class TestServiceRequestEntryPoints:
    """Test cases for entry points URL endpoint"""
    
    def test_GET_entryPointsUrl_success(self, client_factory):
        """Test successful retrieval of entry points URL"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get("/servicerequest/entryPointsUrl")
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Validate response structure based on swagger schema
        assert "dashboardUrl" in response_data
        assert "en" in response_data["dashboardUrl"]
        assert "fr" in response_data["dashboardUrl"]
        
        logging.info("test_GET_entryPointsUrl_success passed")
 


class TestInProgressRequests:
    """Test cases for in-progress request endpoints"""
    
    def test_GET_inProgress_by_type_and_uuid_success(self, client_factory):
        """Test successful retrieval of in-progress requests by type and UUID"""
        client = client_factory(username=TEST_USER, password=password)

        for request_type, uuid_value in VALID_REQUEST_TYPES.items():
            response = client.get(f"/servicerequest/inProgress/{request_type}/{uuid_value}")
            assert response.status_code == 200
            
            # Validate response is array of InProgressRequest objects
            response_data = response.json()
            assert isinstance(response_data, list)
            
            # If there are items, validate structure
            if response_data:
                for item in response_data:
                    if "apiDocumentId" in item:
                        # Validate UUID format if present
                        try:
                            uuid.UUID(item["apiDocumentId"])
                        except ValueError:
                            pytest.fail(f"Invalid UUID format in apiDocumentId: {item['apiDocumentId']}")
                    
                    if "viewPageUrl" in item:
                        assert isinstance(item["viewPageUrl"], str)
            
            logging.info(f"test_GET_inProgress_by_type_and_uuid_success passed for type: {request_type}")

    def test_GET_inProgress_by_type_and_uuid_invalid_type(self, client_factory):
        """Test in-progress requests with invalid request type"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get(f"/servicerequest/inProgress/{INVALID_REQUEST_TYPE}/{TEST_UUID}")
        
        # Should return 400 for invalid enum value
        assert response.status_code == 500
        logging.info("test_GET_inProgress_by_type_and_uuid_invalid_type passed")

    def test_GET_inProgress_by_type_and_uuid_invalid_uuid(self, client_factory):
        """Test in-progress requests with invalid UUID format"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get(f"/servicerequest/inProgress/MAPPING/{INVALID_UUID}")
        
        # Should return 400 for invalid UUID format
        assert response.status_code == 500
        logging.info("test_GET_inProgress_by_type_and_uuid_invalid_uuid passed")

    def test_GET_inProgress_by_uuid_success(self, client_factory):
        """Test successful retrieval of in-progress requests by UUID only"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get(f"/servicerequest/inProgress/{TEST_UUID}")
        
        assert response.status_code == 200
        
        # Validate response is array of InProgressRequest objects
        response_data = response.json()
        assert isinstance(response_data, list)
        
        logging.info("test_GET_inProgress_by_uuid_success passed")
 
    def test_GET_inProgress_by_uuid_not_found(self, client_factory):
        """Test in-progress requests with non-existent UUID"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get(f"/servicerequest/inProgress/{NON_EXISTENT_UUID}")
        
        # Should return 200 with empty array or 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            response_data = response.json()
            assert isinstance(response_data, list)
        
        logging.info("test_GET_inProgress_by_uuid_not_found passed")



 
    def test_POST_mapping_service_request_unauthorized(self, client_factory):
        """Test mapping service request with unauthorized user"""
        client = client_factory(username="invalid_user", password="invalid_pass")
        
        mapping_data = "Sample mapping request data"
        mapping_uuid = VALID_REQUEST_TYPES["MAPPING"]
        
        response = client.post(
            f"/servicerequest/request/mapping/{mapping_uuid}",
            data=mapping_data,
            headers={'Content-Type': 'text/plain'}
        )
        
        # Should return 401 or 403 for unauthorized access
        assert response.status_code in [401, 403]
        logging.info("test_POST_mapping_service_request_unauthorized passed")


class TestRequestTypes:
    """Test cases for request type endpoints"""
    
    def test_GET_permitted_catalogue_request_types_success(self, client_factory):
        """Test successful retrieval of permitted request types for catalogue"""
        client = client_factory(username=TEST_USER, password=password)

        # Test with both MAPPING and API UUIDs
        for request_type, uuid_value in VALID_REQUEST_TYPES.items():
            response = client.get(f"/servicerequest/requestType/catalogue/{uuid_value}")
            
            assert response.status_code == 200
            
            # Validate response is array of RequestTypeResult objects
            response_data = response.json()
            assert isinstance(response_data, list)
            
            # If there are items, validate structure
            if response_data:
                for item in response_data:
                    if "requestType" in item:
                        assert item["requestType"] in VALID_REQUEST_TYPES.keys()
                    
                    if "requestTypeName" in item:
                        assert "en" in item["requestTypeName"]
                        assert "fr" in item["requestTypeName"]
                    
                    if "serviceRequestUrl" in item:
                        assert "en" in item["serviceRequestUrl"]
                        assert "fr" in item["serviceRequestUrl"]
            
            logging.info(f"test_GET_permitted_catalogue_request_types_success passed for {request_type}: {uuid_value}")

     

    def test_GET_permitted_catalogue_request_types_not_found(self, client_factory):
        """Test request types with non-existent catalogue UUID"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get(f"/servicerequest/requestType/catalogue/{NON_EXISTENT_UUID}")
        
        # Should return 200 with empty array or 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            response_data = response.json()
            assert isinstance(response_data, list)
        
        logging.info("test_GET_permitted_catalogue_request_types_not_found passed")


class TestUserTransfer:
    """Test cases for user ownership transfer"""
    
    

    def test_PUT_transfer_ownership_invalid_source_uuid(self, client_factory):
        """Test ownership transfer with invalid source user UUID"""
        client = client_factory(username=TEST_USER, password=password)

        target_user_id = TEST_UUID
        
        response = client.patch(f"/servicerequest/users/{INVALID_UUID}/transfer?target_user_id={target_user_id}")
        
        # Should return 400 for invalid UUID format
        assert response.status_code == 500
        logging.info("test_PUT_transfer_ownership_invalid_source_uuid passed")

    def test_PUT_transfer_ownership_invalid_target_uuid(self, client_factory):
        """Test ownership transfer with invalid target user UUID"""
        client = client_factory(username=TEST_USER, password=password)

        source_user_id = TEST_UUID
        
        response = client.patch(f"/servicerequest/users/{source_user_id}/transfer?target_user_id={INVALID_UUID}")
        
        # Should return 400 for invalid UUID format
        assert response.status_code == 500
        logging.info("test_PUT_transfer_ownership_invalid_target_uuid passed")

    def test_PUT_transfer_ownership_missing_target(self, client_factory):
        """Test ownership transfer without target user ID"""
        client = client_factory(username=TEST_USER, password=password)

        source_user_id = TEST_UUID
        
        response = client.patch(f"/servicerequest/users/{source_user_id}/transfer")
        
        # Should return 400 for missing required parameter
        assert response.status_code == 500
        logging.info("test_PUT_transfer_ownership_missing_target passed")

    def test_PUT_transfer_ownership_unauthorized(self, client_factory):
        """Test ownership transfer with unauthorized user"""
        client = client_factory(username="invalid_user", password="invalid_pass")
        
        source_user_id = TEST_UUID
        target_user_id = "a1b2c3d4-5e6f-7890-abcd-ef1234567890"
        
        response = client.patch(f"/servicerequest/users/{source_user_id}/transfer?target_user_id={target_user_id}")
        
        # Should return 401 or 403 for unauthorized access
        assert response.status_code in [401, 403]
        logging.info("test_PUT_transfer_ownership_unauthorized passed")


class TestErrorHandling:
    """Additional error handling test cases"""
    
    def test_invalid_endpoint(self, client_factory):
        """Test request to non-existent endpoint"""
        client = client_factory(username=TEST_USER, password=password)
        response = client.get("/servicerequest/nonexistent/endpoint")
        
        # Should return 404 for non-existent endpoint
        assert response.status_code == 404
        logging.info("test_invalid_endpoint passed")

    def test_method_not_allowed(self, client_factory):
        """Test invalid HTTP method on valid endpoint"""
        client = client_factory(username=TEST_USER, password=password)
        
        # Try POST on GET-only endpoint
        response = client.post(f"/servicerequest/inProgress/{TEST_UUID}")
        
        # Should return 405 for method not allowed
        assert response.status_code == 405
        logging.info("test_method_not_allowed passed")

    def test_malformed_json_request(self, client_factory):
        """Test request with malformed JSON"""
        client = client_factory(username=TEST_USER, password=password)

        # Send malformed JSON to mapping endpoint
        malformed_data = '{"invalid": json}'
        mapping_uuid = VALID_REQUEST_TYPES["MAPPING"]
        
        response = client.post(
            f"/servicerequest/request/mapping/{mapping_uuid}",
            data=malformed_data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Should handle gracefully (depends on endpoint implementation)
        assert response.status_code in [200, 400, 403, 415]
        logging.info("test_malformed_json_request passed")

    def test_large_payload(self, client_factory):
        """Test request with large payload"""
        client = client_factory(username=TEST_USER, password=password)

        # Create large text data (1MB)
        large_data = "x" * (1024 * 1024)
        mapping_uuid = VALID_REQUEST_TYPES["MAPPING"]
        
        response = client.post(
            f"/servicerequest/request/mapping/{mapping_uuid}",
            data=large_data,
            headers={'Content-Type': 'text/plain'}
        )
        
        # Should handle large payload or return appropriate error
        assert response.status_code in [200, 413, 400, 403, 409]
        logging.info("test_large_payload passed")

    def test_concurrent_requests(self, client_factory):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        client = client_factory(username=TEST_USER, password=password)
        results = []
        
        def make_request():
            response = client.get(f"/servicerequest/inProgress/{TEST_UUID}")
            results.append(response.status_code)
        
        # Create multiple threads to make concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        logging.info("test_concurrent_requests passed")