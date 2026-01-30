# booking.py
from data import drivers_by_location, trip_history
from search import search_location
from trip import download_invoice

def book_cab(customer_name):
    search = input("Enter pickup location (search): ")
    suggestions = search_location(search)

    if not suggestions:
        print("❌ No matching locations found")
        return

    print("\nSuggested Locations:")
    for i, loc in enumerate(suggestions, 1):
        print(f"{i}. {loc}")

    choice = int(input("Select location number: "))
    pickup = suggestions[choice - 1]

    # Safe check for drivers
    if pickup not in drivers_by_location or not drivers_by_location[pickup]:
        print("❌ No drivers available at this location")
        return

    driver = drivers_by_location[pickup].pop()   # Assign driver

    drop = input("Enter drop location: ")
    if pickup == drop:
        print("❌ Pickup and drop cannot be the same")
        drivers_by_location[pickup].add(driver)
        return

    distance = float(input("Enter distance in km: "))
    fare = distance * 20   # ₹20 per km

    trip = {
        "customer": customer_name,
        "driver": driver,
        "route": (pickup, drop),
        "distance": distance,
        "fare": fare,
        "status": "Booked"
    }

    trip_history.append(trip)

    print("\n🚕 Cab Booked Successfully!")
    print(f"Driver Assigned: {driver}")
    print(f"Route: {pickup} → {drop}")
    print(f"Distance: {distance} km | Fare: ₹{fare}")

    # --- START RIDE ---
    start = input("Start the ride? (y/N): ")
    if start.lower() == "y":
        print("Ride started ✅")
        end = input("End the ride? (y/N): ")
        if end.lower() == "y":
            trip["status"] = "Completed"
            print("Ride ended ✅")
            payment = input("Payment successful? (Y/N): ")
            if payment.lower() == "y":
                print("Payment completed ✅")
            else:
                print("Payment failed ❌")
            # Make driver available again
            drivers_by_location[pickup].add(driver)
            # Auto download invoice
            download_invoice(trip)
        else:
            print("Ride not ended yet")
    else:
        print("Ride not started")
