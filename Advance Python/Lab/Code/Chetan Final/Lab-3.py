import numpy as np
import pandas as pd
from typing import Literal
import traceback
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Centralize file paths here
TRAINS_FILE = r"D:\Ghanu Study\Sem - 5\Advance Python\Lab\Code\files\trains.csv"
PASSENGERS_FILE = r"D:\Ghanu Study\Sem - 5\Advance Python\Lab\Code\files\passengers.csv"

# Function to print errors
def print_error(e: Exception) -> None:
    tb = traceback.extract_tb(e.__traceback__)
    for filename, line, funcname, text in tb:
        print("-" * 100)
        print(f"Error -> {e}")
        print(f"File -> {filename}")
        print(f"Function -> {funcname}, Line -> {line}")
        print(f"Code -> {text}\n")
        print("-" * 100)

# Fare calculation based on distance
def fare(distance):
    try:
        if distance <= 0:
            raise ValueError(f"Invalid distance {distance}")
        if distance <= 500:
            return distance * 1.5
        elif distance <= 1000:
            return distance * 1.2
        else:
            return distance * 1.0
    except Exception as e:
        print_error(e)

# Booking function
def book(name: str, passengers: pd.DataFrame, trains: pd.DataFrame) -> Literal[0, 1]:
    try:
        passenger_index = np.where(passengers["Passenger Name"] == name)[0]
        train_id = passengers.loc[passenger_index, "Train ID"].iloc[0]
        num = passengers.loc[passenger_index, "Number of Tickets"].iloc[0]

        if num <= 0:
            raise ValueError(f"Invalid number of tickets: {num}")
        if train_id not in trains["Train ID"].values:
            raise ValueError(f"No train with ID {train_id}")

        train_index = np.where(trains["Train ID"] == train_id)[0]
        available = trains.loc[train_index, "Total Seats"].iloc[0]

        if num > available:
            raise ValueError(f"Not enough seats in train {train_id}")

        trains.loc[train_index, "Total Seats"] -= num
        passengers.loc[passenger_index, "Fare"] = num * trains.loc[train_index, "Single Fare"].iloc[0]
        passengers.loc[passenger_index, "Status"] = "Success"
        return 0
    except Exception as e:
        print_error(e)
        passengers.loc[passenger_index, "Status"] = "Failed"
        return 1

# Report 1: Train details
def print_report1(trains: pd.DataFrame, filename: str) -> None:
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        margin = 60
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, height - 30, "Details of Trains")
        y = height - margin
        c.setFont("Helvetica", 12)
        for i, train in trains.iterrows():
            c.drawString(50, y, f"{i+1}) {train['Train Name']}")
            y -= 20
            c.drawString(70, y, f"Source -> {train['Source Station']}")
            y -= 20
            c.drawString(70, y, f"Destination -> {train['Destination Station']}")
            y -= 20
            c.drawString(70, y, f"Seats Available -> {train['Total Seats']}")
            y -= 30
            if y < margin:
                c.showPage()
                y = height - margin
        c.save()
    except Exception as e:
        print_error(e)

# Report 2: Revenue and booking summary
def print_report2(passengers: pd.DataFrame, trains: pd.DataFrame, filename: str) -> None:
    try:
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        margin = 60
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, height - 30, "Fare Collection Report")
        y = height - margin
        c.setFont("Helvetica", 12)
        for i, train in trains.iterrows():
            train_id = train["Train ID"]
            success = np.where((passengers["Train ID"] == train_id) & (passengers["Status"] == "Success"))[0]
            failed = np.where((passengers["Train ID"] == train_id) & (passengers["Status"] == "Failed"))[0]
            c.drawString(50, y, f"{i+1}) {train['Train Name']}")
            y -= 20
            c.drawString(70, y, f"Successful Bookings -> {success.shape[0]}")
            y -= 20
            c.drawString(70, y, f"Failed Bookings -> {failed.shape[0]}")
            y -= 20
            c.drawString(70, y, f"Total Fare Collected -> {np.sum(passengers.loc[success, 'Fare'])}")
            y -= 30
            if y < margin:
                c.showPage()
                y = height - margin
        c.save()
    except Exception as e:
        print_error(e)

# Main
def main():
    try:
        # Always load from files folder
        trains = pd.read_csv(TRAINS_FILE)
        passengers = pd.read_csv(PASSENGERS_FILE)

        passengers["Status"] = "Pending"
        passengers["Fare"] = -1
        trains["Single Fare"] = trains["Distance"].apply(fare)
        passengers["Passenger Name"].apply(book, args=(passengers, trains,))

        print_report1(trains, "report1.pdf")
        print_report2(passengers, trains, "report2.pdf")
        print("✅ Reports generated successfully!")
    except Exception as e:
        print_error(e)

if __name__ == "__main__":
    main()
