import requests
import logging,json
from config.config import BASE_URL, AUTH_ENDPOINT, USERNAME, PASSWORD


class ApiMethods:
    def __init__(self, config):
        self.base_url = config['base_url']
        self.token = config['token']
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get(self, endpoint):
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        response = requests.get(url, headers=headers)
        self.log_response(response)
        return response

    def post(self, endpoint, data):
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        response = requests.post(url, json=data, headers=headers)
        self.log_response(response)
        return response

    def put(self, endpoint, data, custom_headers=None):
        """Send a PUT request with custom headers if provided."""
        url = f"{self.base_url}{endpoint}"

        # Default headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Include token in headers if provided and no custom headers override it
        if self.token and not custom_headers:
            headers['Cookie'] = f'token={self.token}'

        # If custom headers are provided, update or override the headers dictionary
        if custom_headers:
            headers= custom_headers
        response = requests.put(url, headers=headers, data=json.dumps(data))
        return response

    def delete(self, endpoint, custom_headers=None):
        """Send a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        headers = self.headers.copy()
        if custom_headers:
            headers = custom_headers
        response = requests.delete(url, headers=headers)


        return response

    def log_response(self, response):
        """Log response status and body."""
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.text}")
        if response.status_code >= 400:
            logging.error(f"Error: {response.status_code} - {response.text}")

