
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
