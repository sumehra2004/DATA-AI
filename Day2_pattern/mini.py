friends_data = []
n = int(input("Enter number of friends went to trip: "))
for i in range(n):
    print(f"\nFriend {i+1} details")
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    bills_count = int(input("Enter number of bills: "))
    bills = []
    for j in range(bills_count):
        amount = float(input(f"Enter bill {j+1} amount: "))
        bills.append(amount)
    ph = phone[:2] + "******" + phone[-2:]
    friends_data.append({
        "name": name.strip(),
        "phone": ph,
        "bills": bills
    }
    )
def trip_expense(friends_data):
    result = {}
    for friend in friends_data:
        name = friend["name"]
        phone = friend["phone"]
        bills = friend["bills"]
        total = sum(bills)
        result[name] = {
            "Phone": phone,
            "Total Spent": total
        }
    return result
result = trip_expense(friends_data)
print("\n--- Trip Expense Summary ---")
for name, details in result.items():
    print(f"{name} ({details['Phone']}) spent ₹{details['Total Spent']}")
