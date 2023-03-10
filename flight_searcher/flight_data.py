from datetime import datetime, date, timedelta
import requests, toml
from pathlib import Path

api_file_path = Path(__file__).parent.parent / "api_keys.toml"
with open(api_file_path, "r") as f:
    config = toml.load(f)
    
api_key = config["api_keys"]["kiwi_key"]

tomorrow = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
end_date = (date.today() + timedelta(weeks=40)).strftime("%d/%m/%Y")
search_url = "https://tequila-api.kiwi.com/v2/search"
headers = {"apikey": api_key}
parameters = {
    "fly_from": "YHZ",
    "fly_to": "",
    "dateFrom": tomorrow,
    "dateTo": end_date,
    "adults": 1,
    "curr": "CAD",
    "sort": "price",
    "asc": 1,
    "limit": 1,
    "flight_type": "round",
    "nights_in_dst_from": 5,
    "nights_in_dst_to": 21,
    "partner_market": "ca",
    "max_stopovers": 4,
    "select_airlines": "F8,WO,Y9",
    "select_airlines_exclude": "true"
}


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, iata, city):
        self.iata = iata
        self.parameters = parameters
        self.parameters["fly_to"] = self.iata
        self.city = city
        self.results = requests.get(f"{search_url}", headers=headers, params=self.parameters).json()
        # print(f'url:{search_url}\nheaders: {headers}\nparams: {self.parameters}')
        self.num_results = self.results['_results']

    # Gets cheapest flight
    def scrape_flight_info(self):
        result = self.results["data"][0]
        self.price = result["price"]
        self.nights = result["nightsInDest"]
        self.departure = datetime.strptime(
            result["local_departure"].split("T")[0], "%Y-%m-%d"
        )
        self.link = result["deep_link"]

    def get_num_results(self):
        return self.num_results

    def get_price(self):
        return self.price

    def get_link(self):
        return self.link

    def get_return_date(self):
        duration = self.nights
        return_date = (self.departure + timedelta(days=duration)).strftime(
            "%a, %b %d, %Y"
        )
        return return_date

    def get_departure(self):
        return self.departure.strftime("%a, %b %d, %Y")
