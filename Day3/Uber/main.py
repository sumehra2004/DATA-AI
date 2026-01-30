from booking import book_cab
from trip import complete_trip, view_trips

while True:
    print("\n------ UBER APPLICATION ------")
    print("1. Book Cab")
    print("2. Complete Trip")
    print("3. View Last Trip & Download Invoice")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter customer name: ")
        book_cab(name)

    elif choice == "2":
        complete_trip()

    elif choice == "3":
        view_trips()

    elif choice == "4":
        print("👋 Thank you for using Uber")
        break

    else:
        print("❌ Invalid choice")