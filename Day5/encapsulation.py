
class BankAccount:
    def __init__(self, name, acc_no, balance):
        self.name = name
        self.acc_no = acc_no
        self.__balance = balance   
        self.__pin = "1234"

    def check_pin(self, pin):
        return self.__pin == pin

    def get_balance(self):
        return self.__balance

    def deposit(self, amt):
        self.__balance += amt
        print("Deposited:", amt)

    def withdraw(self, amt):
        if amt <= self.__balance:
            self.__balance -= amt
            print("Withdrawn:", amt)
        else:
            print("Insufficient balance")

class SavingsAccount(BankAccount):
    def account_type(self):
        return "Savings Account"


class CurrentAccount(BankAccount):
    def account_type(self):
        return "Current Account"

class Transaction:
    def process(self, amount, *args):
        if len(args) == 0:
            print("Payment of", amount)
        elif len(args) == 1:
            print("Transfer of", amount, "to account", args[0])


accounts = {}
transaction = Transaction()

while True:
    print("\n--- BANK MENU ---")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Transaction Demo")
    print("6. Exit")

    choice = input("Enter choice: ")


    if choice == '1':
        name = input("Name: ")
        acc_no = input("Account Number: ")
        balance = float(input("Initial Balance: "))
        acc_type = input("Account Type (S/C): ")

        if acc_type.lower() == 's':
            accounts[acc_no] = SavingsAccount(name, acc_no, balance)
        else:
            accounts[acc_no] = CurrentAccount(name, acc_no, balance)

        print("Account created successfully!")

    elif choice == '2':
        acc_no = input("Account Number: ")
        pin = input("PIN: ")
        amt = float(input("Amount: "))

        if accounts[acc_no].check_pin(pin):
            accounts[acc_no].deposit(amt)
        else:
            print("Wrong PIN")

    elif choice == '3':
        acc_no = input("Account Number: ")
        pin = input("PIN: ")
        amt = float(input("Amount: "))

        if accounts[acc_no].check_pin(pin):
            accounts[acc_no].withdraw(amt)
        else:
            print("Wrong PIN")

    elif choice == '4':
        acc_no = input("Account Number: ")
        pin = input("PIN: ")

        if accounts[acc_no].check_pin(pin):
            print("Balance:", accounts[acc_no].get_balance())
        else:
            print("Wrong PIN")

    elif choice == '5':
        amt = float(input("Amount: "))
        to_acc = input("Transfer account (optional): ")

        if to_acc:
            transaction.process(amt, to_acc)
        else:
            transaction.process(amt)

    elif choice == '6':
        print("Thank you ")
        break

    else:
        print("Invalid choice")
