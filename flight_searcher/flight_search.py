import requests, toml
from pathlib import Path

api_file_path = Path(__file__).parent.parent / "api_keys.toml"
with open(api_file_path, "r") as f:
    config = toml.load(f)
    
api_key = config["api_keys"]["kiwi_key"]

# receives city name and responds with testing
headers = {"apikey": api_key}


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, city):
        self.city = city
        parameters = {"term": self.city}
        url = "https://tequila-api.kiwi.com"
        results = requests.get(
            f"{url}/locations/query", headers=headers, params=parameters
        )
        iata_code = results.json()["locations"][0]["code"]
        self.iata = iata_code

    def get_iata(self):
        return self.iata
