#! /usr/bin/env python3
# This file will need to use the DataManager, FlightData, NotificationManager classes to achieve the program requirements.
from flight_data import FlightData
from notification_manager import NotificationManager, EmailManager
import csv_reader, csv
from pathlib import Path

DISCOUNT_THRESHOLD = 0.25

# Get the absolute path to the current Python script
script_path = Path(__file__).resolve().parent

message_list = []
updated_rows = []
rows = csv_reader.read_csv()
city_flight_data = [[city, iata, desired_price, avg_price, queries] for [_, city, iata, desired_price, avg_price, queries] in rows]
for row in city_flight_data:
    city, iata_code, desired_price, average, queries = row
    average = float(average)
    desired_price = float(desired_price)
    flight_data = FlightData(iata_code, city)
    if flight_data.get_num_results() == 0:
        updated_rows.append(row)
        print(f'No results found for {city}')
    else:
        # increment query count
        queries = int(queries) + 1
        flight_data.scrape_flight_info()
        lowest_price = float(flight_data.get_price())
        new_average = round(float(average*(queries-1)/queries+lowest_price/queries),3)
        row = [city, iata_code, desired_price, new_average, queries]
        updated_rows.append(row)
        print(f'{city} price: ${lowest_price}')
        
        if (lowest_price <= desired_price) or (lowest_price <= average*(1-DISCOUNT_THRESHOLD)):
            web_link = flight_data.get_link()
            departure_date = flight_data.get_departure()
            return_date = flight_data.get_return_date()
            message_list.append(
                (city, lowest_price, web_link, departure_date, return_date)
            )


with open(script_path/'flight_data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(updated_rows)


if len(message_list) > 0:
    html_deals = NotificationManager(message_list).get_message()
    EmailManager(html_deals)
    print("Email Sent")
else:
    print("No Results")
