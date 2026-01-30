print("Welcome to Zomato!")
print("Today's Special: Free Delivery on all orders!")
print("Menu:\n 1. Pizza \n 2. Burger \n 3. Pasta \n 4. Salad \n 5. Dessert \n 6. Biryani")
PRICE_PER_ITEM = 0  
print("Enter ur choice from the menu:")
choice = int(input())   
if choice == 1:
    PRICE_PER_ITEM = 250        
elif choice == 2:
    PRICE_PER_ITEM = 150
elif choice == 3:
    PRICE_PER_ITEM = 200
elif choice == 4:   
    PRICE_PER_ITEM = 100
elif choice == 5:
    PRICE_PER_ITEM = 120    
try:
    items = int(input("How many items do you want to order? "))

    if items == 0:
        raise ZeroDivisionError()

    total_bill = items * PRICE_PER_ITEM

except ValueError:
    print("Invalid input! Please enter a number.")

except ZeroDivisionError:
    print("You cannot order 0 items.")

else:
    print(f"Order placed successfully!")
    print(f"Total bill: ₹{total_bill}")

finally:
    print("Thank you for using Zomato!")
