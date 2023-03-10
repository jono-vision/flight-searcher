import csv
from pathlib import Path

def read_csv():
    city_flight_list = []
    data_path = _get_flight_data_filepath()
    with open(data_path) as f:
        reader = csv.reader(f)
        # headers = next(reader)
        for i, row in enumerate(reader):
            city_flight_list.append([i, *row])
    return city_flight_list

def _get_flight_data_filepath():
    data_filepath = Path(__file__).resolve().parent / 'flight_data.csv'
    if not data_filepath.is_file():
        print('No flight data found creating new file')
        data_filepath.touch()
    return data_filepath