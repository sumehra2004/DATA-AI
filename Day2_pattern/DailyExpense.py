def daily_expense_tracker(expenses):
    total = 0
    summary = {}

    for item in expenses:
        name = item["name"]
        amount = item["amount"]
        total += amount
        summary[name] = amount

    return summary, total

expenses = []

n = int(input("Enter number of expenses for today: "))

for i in range(n):
    print(f"\nExpense {i+1}")
    name = input("Enter expense name: ")
    amount = float(input("Enter amount spent: "))

    expenses.append({
        "name": name,
        "amount": amount
    })

result, total_spent = daily_expense_tracker(expenses)


print("\n--- Daily Expense Summary ---")
for name, amount in result.items():
    print(f"{name} : ₹{amount}")

print(f"\nTotal amount spent today: ₹{total_spent}")
