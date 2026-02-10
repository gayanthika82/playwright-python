import json
from typing import Dict, Any

class ResponseFormatter:
    """Utility class for pretty printing HTTP responses"""
    
    @staticmethod
    def print_pretty_response(method: str, url: str, headers: Dict, response, request_data=None):
        """
        Print HTTP request and response in a nicely formatted way
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            headers: Request headers
            response: Response object
            request_data: Request data (for POST/PUT)
        """
        print("=" * 80)
        print(f"🌐 {method.upper()} REQUEST")
        print("=" * 80)
        
        # Request details
        print(f"📍 URL: {url}")
        print(f"📋 Request Headers:")
        ResponseFormatter._print_dict_pretty(headers, indent=2)
        
        if request_data:
            print(f"📝 Request Data:")
            if isinstance(request_data, dict):
                ResponseFormatter._print_dict_pretty(request_data, indent=2)
            else:
                print(f"  {request_data}")
        
        print("-" * 40)
        
        # Response details
        status_emoji = "✅" if 200 <= response.status_code < 300 else "❌"
        print(f"{status_emoji} Response Status: {response.status_code}")
        
        print(f"📨 Response Headers:")
        ResponseFormatter._print_dict_pretty(dict(response.headers), indent=2)
        
        print(f"📄 Response Body:")
        ResponseFormatter._print_response_body(response)
        
        print("=" * 80)
        print()
    
    @staticmethod
    def _print_dict_pretty(data: Dict, indent: int = 0):
        """Print dictionary in a pretty format"""
        for key, value in data.items():
            spaces = " " * indent
            if isinstance(value, dict):
                print(f"{spaces}{key}:")
                ResponseFormatter._print_dict_pretty(value, indent + 2)
            else:
                # Truncate long values (like tokens)
                if isinstance(value, str) and len(value) > 100:
                    display_value = f"{value[:50]}...{value[-20:]}"
                else:
                    display_value = value
                print(f"{spaces}{key}: {display_value}")
    
    @staticmethod
    def _print_response_body(response):
        """Print response body in a formatted way"""
        try:
            # Try to parse as JSON for pretty printing
            json_data = response.json()
            print("  " + json.dumps(json_data, indent=2, ensure_ascii=False))
        except (json.JSONDecodeError, ValueError):
            # If not JSON, print as text
            body = response.text
            if body.strip():
                # Print each line with indentation
                for line in body.split('\n'):
                    print(f"  {line}")
            else:
                print("  (empty response body)")
    
    @staticmethod
    def print_simple_response(response):
        """Print a simplified version of the response"""
        status_emoji = "✅" if 200 <= response.status_code < 300 else "❌"
        print(f"{status_emoji} Status: {response.status_code}")
        
        if response.text.strip():
            try:
                json_data = response.json()
                print("📄 JSON Response:")
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
            except:
                print("📄 Text Response:")
                print(response.text)
        else:
            print("📄 Empty response body")
        print("-" * 40)
