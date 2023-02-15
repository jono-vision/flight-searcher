#! /usr/bin/env python3
# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager, EmailManager
import csv_gui

DISCOUNT_THRESHOLD = 0.25

data = DataManager()

message_list = []
rows = csv_gui.read_csv()
for i, row in enumerate(rows):
    city, iata_code, desired_price, average, queries = row
    print(city)
    flight_data = FlightData(iata_code, city)
    if flight_data.get_num_results() == 0:
        continue
    else:
        flight_data.scrape_flight_info()
        lowest_price = flight_data.get_price()
        # increment query count
        queries += 1
        if (lowest_price <= desired_price) or (lowest_price <= average*(1-DISCOUNT_THRESHOLD)):
            web_link = flight_data.get_link()
            departure_date = flight_data.get_departure()
            return_date = flight_data.get_return_date()
            message_list.append(
                (city, lowest_price, web_link, departure_date, return_date)
            )

if len(message_list) > 0:
    html_deals = NotificationManager(message_list).get_message()
    EmailManager(html_deals)
    print("Email Sent")
else:
    print("No Results")
