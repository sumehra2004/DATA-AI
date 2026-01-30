from data import drivers_by_location, trip_history
from datetime import datetime

def complete_trip():
    if len(trip_history) == 0:
        print("No trips to complete")
        return

    last_trip = trip_history[-1]
    pickup = last_trip["route"][0]

    drivers_by_location[pickup].add(last_trip["driver"])
    last_trip["status"] = "Completed"

    print("✅ Trip completed")

def download_invoice(trip):
    filename = f"invoice_{trip['customer']}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("--------- UBER TRIP INVOICE ---------\n")
        f.write(f"Customer : {trip['customer']}\n")
        f.write(f"Driver   : {trip['driver']}\n")
        f.write(f"Pickup   : {trip['route'][0]}\n")
        f.write(f"Drop     : {trip['route'][1]}\n")
        f.write(f"Distance : {trip['distance']} km\n")
        f.write(f"Fare     : ₹{trip['fare']}\n")
        f.write(f"Status   : {trip['status']}\n")
        f.write(f"Date     : {datetime.now()}\n")
        f.write("------------------------------------\n")
        f.write("Thank you for riding with Uber 🚕\n")
    print(f"📄 Invoice downloaded: {filename}")

def view_trips():
    if len(trip_history) == 0:
        print("No trips found")
        return

    last_trip = trip_history[-1]

    print("\nLast Trip")
    print("Customer :", last_trip["customer"])
    print("Driver   :", last_trip["driver"])
    print("Route    :", last_trip["route"][0], "→", last_trip["route"][1])
    print("Distance :", last_trip["distance"], "km")
    print("Fare     : ₹", last_trip["fare"])
    print("Status   :", last_trip["status"])

    download_invoice(last_trip)
