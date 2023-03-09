# Flight Deal Finder

## About

This program helps users find flight deals by scraping flight information for desired cities and notifying the user if the price is below their desired price or below the average price by a certain discount threshold.

## Initial Set Up

On the initial setup the destinations and prices will need to be set. To do this in command prompt navigate to the directory flight_searcher directory where the csv_gui.py file is located and run the following command.

```
python3 csv_gui
```

This will open a gui for you to add destinations and modify existing destinations. Unfortunately the only way to delete records is by deleting rows from the csv file. To modify existing you simply double click the row you want to modify which will then take you to the edit screen.

## Usage

The main.py file can be run to start the program. The user will be prompted to enter the desired cities and prices in a GUI. The program will then scrape flight information for the cities entered and notify the user if a flight deal is found.

If a flight deal is found, the user will receive an email notification. If no flight deals are found, the program will print "No Results".

The flight data is stored in flight_data.csv. This file is automatically created if it does not exist.

## Notes

This program uses the IATA codes to search for flights. Therefore, it is recommended to input the full name of the city to obtain the correct IATA code.
