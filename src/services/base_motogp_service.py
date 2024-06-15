import requests

class MotoGPBaseService:
    def __init__(self, api_url):
        self.api_url = api_url

    def _get_data(self, endpoint: str) -> dict:
        try:
            response = requests.get(f"{self.api_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except ValueError as e:
            print(f"Error parsing response: {e}")
            return None
