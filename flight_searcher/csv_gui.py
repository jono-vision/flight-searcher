import tkinter as tk
from tkinter import ttk
import csv
from flight_search import FlightSearch

def _save_to_csv(city, iata_code, desired_price, average, queries):
    with open("flight_data.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([city, iata_code, desired_price, average, queries])

# Add new entry to csv
def update_csv(avg_price, queries, iata_code):
    global row_id
    city = city_entry.get()
    desired_price = price_entry.get()
    if iata_code == '':
        iata_code = get_iata_code(city)
    if row_id == '': # New Entry
        # print(f'row id: {row_id}')
        avg_price = 0
        queries = 0
        _save_to_csv(city, iata_code, desired_price, avg_price, queries)
    else:
        queries = queries
        rows = read_csv()
        del rows[row_id]
        row_id = ''
        
        city_flight_data = [[city, iata, desired_price, avg_price, queries] for [_, city, iata, desired_price, avg_price, queries] in rows]
        new_add = [city, iata_code, desired_price, avg_price, queries]
        iata_code = ''
        city_flight_data.append(new_add)
        with open('flight_data.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(city_flight_data)
    # reset values
    city_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)

def get_iata_code(city):
    city = city_entry.get()
    flightsearch = FlightSearch(city)
    return flightsearch.get_iata()

def read_csv():
    city_flight_list = []
    with open("flight_data.csv") as f:
        reader = csv.reader(f)
        # headers = next(reader)
        for i, row in enumerate(reader):
            city_flight_list.append([i, *row])
    return city_flight_list

def show_frame(frame):
    frame_display.grid_forget()
    frame_home.grid_forget()
    frame.grid()

# def delete_row(event):
#     print('Delete')
#     selected = tree.selection()
#     for item in selected:
#         tree.delete(item)
#     with open('flight_data.csv', 'r') as f:
#         rows = list(csv.reader(f))
#     for i, row in enumerate(selected):
#         del rows[i]
#     with open('flight_data.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerows(rows)

def display_rows():
    show_frame(frame_display)
    rows = read_csv()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5]))

def edit_row(event):
    global row_id, queries, avg_price, iata_code
    for entry in entry_list:
        entry.delete(0, tk.END)
    # Get the selected item
    item = tree.selection()[0]
    show_frame(frame_home)

    # Get the values of the selected item
    selection_id, selection_city, selection_iata, selection_desired_price, selection_average_price, selection_queries = tree.item(item)["values"]
    row_id = selection_id
    queries = selection_queries
    avg_price = selection_average_price
    iata_code = selection_iata
    show_frame(frame_home)

    # update entries with the selection clicked on
    city_entry.insert(0, selection_city)
    price_entry.insert(0, selection_desired_price)

if __name__ == "__main__":
    entry_list = []
    row_id = ''
    queries = 0
    avg_price = ''
    iata_code = ''

    root = tk.Tk()
    frame_home = tk.Frame(root)
    frame_home.grid(row=0, column=0)

    frame_display = tk.Frame(root)
    frame_display.grid(row=0, column=0)

    tree = ttk.Treeview(frame_display, columns=("col0","col1", "col2", "col3","col4", "col5"), show="headings")
    tree.heading("col0", text="ID")
    tree.heading("col1", text="City")
    tree.heading("col2", text="IATA Code")
    tree.heading("col3", text="Desired Price")
    tree.heading("col4", text="average")
    tree.heading("col5", text="queries")

    tree.column("col0",width=30, stretch=False, anchor="center")
    tree.column("col1",width=150, stretch=False)
    tree.column("col2",width=100, stretch=False, anchor="center")
    tree.column("col3",width=100, stretch=False, anchor="center")
    tree.column("col4",width=100, stretch=False, anchor="center")
    tree.column("col5",width=0, stretch=False, anchor="center")
    tree.grid(row=1, column=0)

    tree.bind("<Double-1>", edit_row)
    # Bind right-click event to delete_selected_row function
    # tree.bind("<BackSpace>", delete_row)

    display_button = tk.Button(frame_home, text="Display Rows", command=display_rows)
    display_button.grid(row=0, column=0)

    city_label = tk.Label(frame_home, text="City:")
    city_label.grid(row=1, column=0)

    city_entry = tk.Entry(frame_home)

    city_entry = tk.Entry(frame_home)
    city_entry.grid(row=1, column=1)
    entry_list.append(city_entry)


    price_label = tk.Label(frame_home, text="Desired Price:")
    price_label.grid(row=4, column=0)

    price_entry = tk.Entry(frame_home)
    price_entry.grid(row=4, column=1)
    entry_list.append(price_entry)

    save_button = tk.Button(frame_home, text="Save", command=lambda: update_csv(avg_price,queries,iata_code))
    save_button.grid(row=5, column=1)

    back_button = tk.Button(frame_display, text="Back", command=lambda: show_frame(frame_home))
    back_button.grid(row=0, column=0)

    frame_home.tkraise()

    root.mainloop()
