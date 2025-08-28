import pandas as pd

TRAINS_FILE = r"D:\Ghanu Study\Sem - 5\Advance Python\Lab\Code\files\trains.csv"
PASSENGERS_FILE = r"D:\Ghanu Study\Sem - 5\Advance Python\Lab\Code\files\passengers.csv"

def fare(distance):
    if distance <= 0:
        return 0
    elif distance <= 500:
        return distance * 1.5
    elif distance <= 1000:
        return distance * 1.2
    else:
        return distance * 1.0

def book(passenger, trains):
    train_id = passenger["Train ID"]
    num_tickets = passenger["Number of Tickets"]
    if num_tickets <= 0:
        return "Failed", 0
    if train_id not in trains["Train ID"].values:
        return "Failed", 0
    train_index = trains[trains["Train ID"] == train_id].index[0]
    available = trains.loc[train_index, "Total Seats"]
    if num_tickets > available:
        return "Failed", 0
    trains.loc[train_index, "Total Seats"] -= num_tickets
    total_fare = num_tickets * trains.loc[train_index, "Single Fare"]
    return "Success", total_fare


def write_reports(trains, passengers):
        with open("report1.txt", "w") as f:
            f.write("=== Train Details ===\n\n")
            for i, train in trains.iterrows():
                f.write(f"{i+1}) {train['Train Name']}\n")
                f.write(f"   Source: {train['Source Station']}\n")
                f.write(f"   Destination: {train['Destination Station']}\n")
                f.write(f"   Seats Available: {train['Total Seats']}\n\n")
        with open("report2.txt", "w") as f:
            f.write("=== Booking & Revenue Report ===\n\n")
            for i, train in trains.iterrows():
                train_id = train["Train ID"]
                success = passengers[(passengers["Train ID"] == train_id) & (passengers["Status"] == "Success")]
                failed = passengers[(passengers["Train ID"] == train_id) & (passengers["Status"] == "Failed")]
                f.write(f"{i+1}) {train['Train Name']}\n")
                f.write(f"   Successful Bookings: {len(success)}\n")
                f.write(f"   Failed Bookings: {len(failed)}\n")
                f.write(f"   Total Fare Collected: {success['Fare'].sum()}\n\n")
    

    
def main():
    trains = pd.read_csv(TRAINS_FILE)
    passengers = pd.read_csv(PASSENGERS_FILE)
    passengers["Status"] = "Pending"
    passengers["Fare"] = 0
    trains["Single Fare"] = trains["Distance"].apply(fare)
    for idx, passenger in passengers.iterrows():
        status, total_fare = book(passenger, trains)
        passengers.at[idx, "Status"] = status
        passengers.at[idx, "Fare"] = total_fare
    write_reports(trains, passengers)
    print("✅ Reports generated successfully! (report1.txt & report2.txt)")

if __name__ == "__main__":
    main()
