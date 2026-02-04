from decorators.access import login_required, registration_required
cart = []
@login_required
def add_product(product):
    cart.append(product)
    print(f"{product} added to cart")
@registration_required
def view_cart():
    print("\nCART ITEMS")
    if not cart:
        print("Cart is empty")
    else:
        for item in cart:
            print("-", item)


while True:
    print("\n===== SHOPPING CART =====")
    print("1. Add Product")
    print("2. View Cart")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        product = input("Enter product name: ")
        add_product(product)

    elif choice == "2":
        view_cart()

    elif choice == "3":
        print("Exiting shopping cart")
        break

    else:
        print("Invalid choice")
