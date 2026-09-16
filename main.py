# Individual Final Project 1
# Creating Menu-Driven Query-Based Dashboard with a Dataset
# Kira Almsberger
# Due 5/3/2026

# --------------- Data Setup and Import Configuration ---------------

import csv
import os
import pandas as pd
import plotly.express as px

# --------------- Data Cleaning and Record Setup ---------------

# Create function for cleaning string/text columns
def clean_text(value):
    if value is None:
        return ""
    return str(value).strip().title()

# Create function for cleaning date column
def clean_date(value):
    if value is None:
        return ""
    return str(value).strip().split(" ")[0]

# Create function for cleaning long/lat aka float columns
def clean_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# Creates a dictionary for a city using provided values
def traffic_stop_record(date, location, latitude, longitude, subject_sex, violation, outcome):
    return {
        'date': clean_date(date),
        'location': clean_text(location),
        "latitude": clean_float(latitude),
        "longitude": clean_float(longitude),
        "subject_sex": clean_text(subject_sex),
        "violation": clean_text(violation),
        "outcome": clean_text(outcome)
    }


# --------------- Data Cleaning and Record Setup ---------------

# Reads traffic stops data from CSV and returns a list of dictionaries
def load_data(filepath):
    stops_list = []

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)

        # Only reads 500 rows
        for row in reader:
            if len(stops_list) >= 500:
                break

            stop = traffic_stop_record(
                row.get("date", ""),
                row.get("location", ""),
                row.get("latitude", ""),
                row.get("longitude", ""),
                row.get("subject_sex", ""),
                row.get("violation", ""),
                row.get("outcome", "")
            )

            if stop["date"] and stop["subject_sex"] and stop["violation"]:
                stops_list.append(stop)

    return stops_list

# Loads selected CSV file and returns traffic stop data
# Saves CSV file path so new entries can be saved
def select_and_load_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, 'wi_madison_2007_dec.csv')

    print("\nLoading selected project dataset:")
    print("wi_madison_2007_dec.csv")

    stops_list = load_data(data_file)
    print(f"{len(stops_list)} records loaded.")

    return stops_list, data_file

# Create new entry in dataset
def save_new_entry(filepath, new_stop):
    fieldnames = [
        "date",
        "location",
        "latitude",
        "longitude",
        "subject_sex",
        "violation",
        "outcome"
    ]

    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(new_stop)

# -------------------- Instructions and Validation of Data --------------------
# User Instructions Function
def display_instructions():
    print("\nInstructions:")
    print("This dashboard analyzes traffic stops in Madison, WI from December 2007")
    print("This dataset is sourced from the Stanford Policing Project.")
    print("Choose the load data option before running queries or graphs.")
    print("Use the add entry option to add a sample traffic stop and save it to the CSV file")
    print("Choose 0 to quit the program.")

# Checks dataset size and prints columns in dashboard by numeric and string values
def validate_dataset(stops_list):
    print("\nDataset Requirement Check:")

    total_records = len(stops_list)
    print(f"Total records loaded: {total_records}")

    if 50 <= total_records <= 500:
        print("Record count meets the requirement of 50 to 500 rows.")
    else:
        print("Warning: record count should be between 50 and 500 rows.")

    print("Selected columns used:")
    print("Date, Location, Latitude, Longitude, Subject Sex, Violation, Outcome")
    print("String fields: Date, Location, Subject Sex, Violation, Outcome")
    print("Numeric fields: Latitude, Longitude")


# -------------------- Add New Dataset Entry --------------------

def add_new_stop_entry(filepath, stops_list):
    print("\nAdd a New Traffic Stop Entry")

    date = input("Date, for example 2007-12-15: ")
    location = input("Location: ")
    latitude = input("Latitude: ")
    longitude = input("Longitude: ")
    subject_sex = input("Subject sex, Male or Female: ")
    violation = input("Violation: ")
    outcome = input("Outcome, for example Warning or Citation: ")

    new_stop = traffic_stop_record(
        date,
        location,
        latitude,
        longitude,
        subject_sex,
        violation,
        outcome
    )

    stops_list.append(new_stop)
    save_new_entry(filepath, new_stop)

    print("New traffic stop entry saved.")

# -------------------- Text-Based Menu Functions --------------------
# Required: 3 text-based queries and 3 data visualizations

# Displays total number of men and women that were stopped
def menu_total_men_women_stops(stops_list):
    print("\nTotal Number of Traffic Stops by Men and Women-")

    male_stops = 0
    female_stops = 0

    for stop in stops_list:
        sex = stop['subject_sex']
        if sex == 'Male':
            male_stops += 1
        elif sex == 'Female':
            female_stops += 1

    print(f"Men: {male_stops}")
    print(f"Women: {female_stops}")

# Displays top 5 days in December with most traffic stops
def menu_top_5_days_most_stops(stops_list):
    print("\nTop 5 Days with the Most Traffic Stops-")

    df = pd.DataFrame(stops_list)
    top_days = df["date"].value_counts().head(5)

    for date, count in top_days.items():
        print(f"{date}: {count} stops")

# Displays top 5 most common traffic stop locations
def menu_top_5_locations(stops_list):
    print("\nTop 5 Most Common Traffic Stop Locations:")

    df = pd.DataFrame(stops_list)
    df = df[df["location"] != ""]

    top_locations = df["location"].value_counts().head(5)

    for location, count in top_locations.items():
        print(f"{location}: {count} stops")

# Displays top 5 most common traffic stop violations
def menu_top_5_violations(stops_list):
    print("\nTop 5 Most Common Traffic Stop Violations:")

    df = pd.DataFrame(stops_list)
    df = df[df["violation"] != ""]

    top_violations = df["violation"].value_counts().head(5)

    for violation, count in top_violations.items():
        print(f"{violation}: {count} stops")

# ---------------- Data Visualizations Menu Functions ----------------

# Plots stacked bar chart comparing women and men warnings vs citations
def graph_outcome_by_sex(stops_list):
    df = pd.DataFrame(stops_list)
    # Filter for just Warnings and Citations to keep the graph clean
    df = df[df["outcome"].isin(["Warning", "Citation"])]
    fig = px.histogram(
        df,
        x="subject_sex",
        color="outcome",
        barmode="stack",
        title="Traffic Stop Outcomes by Gender",
        labels={
            "subject_sex": "Subject Sex",
            "outcome": "Outcome"
        }
    )

    fig.show()

# Plots bar chart (or pie chart) of top 10 most common traffic stop violations
def graph_top_10_violations(stops_list):
    df = pd.DataFrame(stops_list)
    df = df[df["violation"] != ""]

    top_10 = df["violation"].value_counts().head(10).reset_index()
    top_10.columns = ["violation_type", "number_of_stops"]

    fig = px.bar(
        top_10,
        x="violation_type",
        y="number_of_stops",
        title="Top 10 Traffic Stop Violations in Madison",
        labels={
            "violation_type": "Violation Type",
            "number_of_stops": "Number of Stops"
        }
    )

    fig.update_layout(xaxis_tickangle=-45)
    fig.show()

# Shows geo map of top 10 traffic stop locations
def graph_top_10_map(stops_list):
    df = pd.DataFrame(stops_list)

    df = df[
        (df["latitude"] != 0.0) &
        (df["longitude"] != 0.0) &
        (df["location"] != "")
    ]

    top_locations = (
        df.groupby(["latitude", "longitude", "location"])
        .size()
        .reset_index(name="count")
        .nlargest(10, "count")
    )

    fig = px.scatter_map(
        top_locations,
        lat="latitude",
        lon="longitude",
        size="count",
        hover_name="location",
        zoom=11,
        center={"lat": 43.0731, "lon": -89.4012},
        map_style="open-street-map",
        title="Top 10 Traffic Stop Locations in Madison"
    )

    fig.show()

# Help make sure data is loaded
def data_loaded(stops_list):
    if len(stops_list) == 0:
        print("\nPlease load the dataset first.")
        return False
    return True

# Menu Function
def run_menu():
    stops_list = []
    data_file = ""

    while True:
        print("\nMadison, WI Traffic Stop Dashboard:")
        print("1) Display Instructions")
        print("2) Load selected project dataset")
        print("3) Check dataset requirements")
        print("4) Add a new traffic stop entry")
        print("5) Total Number of Traffic Stops by Men and Women.")
        print("6) Top 5 days with the most amount of traffic stops.")
        print("7) Top 5 most common traffic stop locations.")
        print("8) Top 5 most common traffic stop violations.")
        print("9) [Graph] Comparing Men vs Women Outcome of Warning or Citation.")
        print("10) [Graph] Top 10 most common traffic stop violations.")
        print("11) [Graph] Top 10 traffic stop locations. (Geo Map)")
        print("0) Quit")

        choice = input("Enter your choice: ")
        if choice == '1':
            display_instructions()

        elif choice == '2':
            stops_list, data_file = select_and_load_dataset()

        elif choice == '3':
            if data_loaded(stops_list):
                validate_dataset(stops_list)

        elif choice == '4':
            if data_loaded(stops_list):
                add_new_stop_entry(data_file, stops_list)

        # Now load queries and graphing functions
        elif choice == '5':
            if data_loaded(stops_list):
                menu_total_men_women_stops(stops_list)
        elif choice == '6':
            if data_loaded(stops_list):
                menu_top_5_days_most_stops(stops_list)
        elif choice == '7':
            if data_loaded(stops_list):
                menu_top_5_locations(stops_list)
        elif choice == '8':
            if data_loaded(stops_list):
                menu_top_5_violations(stops_list)
        elif choice == '9':
            if data_loaded(stops_list):
                graph_outcome_by_sex(stops_list)
        elif choice == '10':
            if data_loaded(stops_list):
                graph_top_10_violations(stops_list)
        elif choice == '11':
            if data_loaded(stops_list):
                graph_top_10_map(stops_list)
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


# Program Start
if __name__ == "__main__":
    run_menu()

