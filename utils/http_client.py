import requests
import logging
from utils.token_store import TokenStore
from utils.response_formatter import ResponseFormatter

class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.default_headers = {}

    def set_header(self, key, value):
        self.default_headers[key] = value

    def clear_header(self, key):
        if key in self.default_headers:
            del self.default_headers[key]

    def get(self, endpoint, headers=None):
        final_headers = {**self.default_headers, **(headers or {})}
        url = f"{self.base_url}{endpoint}"
        
        response = requests.get(url, headers=final_headers)
        
        # Pretty print response
        ResponseFormatter.print_pretty_response("GET", url, final_headers, response)
        
        return response

    def post(self, endpoint, data=None, json=None, headers=None):
        final_headers = {**self.default_headers, **(headers or {})}
        url = f"{self.base_url}{endpoint}"      
        response = requests.post(url, data=data, json=json, headers=final_headers)
        
        # Prepare request data for display
        request_data = {}
        if data:
            request_data["Form Data"] = data
        if json:
            request_data["JSON Data"] = json
        
        # Pretty print response
        ResponseFormatter.print_pretty_response("POST", url, final_headers, response, request_data if request_data else None)
        
        token = response.headers.get("Authorization")
        if token:
            TokenStore.set_token(token)
        return response

    def delete(self, endpoint, headers=None):
        final_headers = {**self.default_headers, **(headers or {})}
        url = f"{self.base_url}{endpoint}"
        
        response = requests.delete(url, headers=final_headers)
        
        # Pretty print response
        ResponseFormatter.print_pretty_response("DELETE", url, final_headers, response)
        
        return response

    def patch(self, endpoint, data=None, json=None, headers=None):
        final_headers = {**self.default_headers, **(headers or {})}
        url = f"{self.base_url}{endpoint}"
        
        response = requests.put(url, data=data, json=json, headers=final_headers)
        
        # Prepare request data for display
        request_data = {}
        if data:
            request_data["Form Data"] = data
        if json:
            request_data["JSON Data"] = json
        
        # Pretty print response
        ResponseFormatter.print_pretty_response("PUT", url, final_headers, response, request_data if request_data else None)
        
        token = response.headers.get("Authorization")
        if token:
            TokenStore.set_token(token)
        return response
