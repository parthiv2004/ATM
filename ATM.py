import datetime
import logging

logging.basicConfig(filename='atm.log', level=logging.INFO)

class ATM:
    def __init__(self):
        self.accounts = {}

    def authenticate(self, user_id, pin):
        if user_id in self.accounts:
            if self.accounts[user_id].check_pin(pin):
                return self.accounts[user_id]
        return None

    def create_account(self):
        user_id = input("Enter User ID: ")
        if user_id not in self.accounts:
            name = input("Enter your name: ")
            pin = input("Enter PIN: ")
            self.accounts[user_id] = Account(user_id, name, pin)
            logging.info(f"Account created: {user_id}")
            print("Account created successfully")
        else:
            print("User ID already exists")

    def start(self):
        print("Welcome to the ATM")
        while True:
            user_id = input("Enter User ID: ")
            pin = input("Enter PIN: ")

            account = self.authenticate(user_id, pin)
            if account:
                print("Authentication successful")
                self.interact(account)
                break
            else:
                print("Invalid User ID or PIN")

    def interact(self, account):
        while True:
            print("\n1. Transactions History")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. Change PIN")
            print("6. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                account.display_transaction_history()
            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                account.withdraw(amount)
            elif choice == "3":
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
            elif choice == "4":
                recipient_id = input("Enter recipient's user ID: ")
                if recipient_id in self.accounts:
                    amount = float(input("Enter amount to transfer: "))
                    account.transfer(amount, self.accounts[recipient_id])
                else:
                    print("Recipient's account not found")
            elif choice == "5":
                new_pin = input("Enter new PIN: ")
                account.change_pin(new_pin)
                print("PIN changed successfully")
            elif choice == "6":
                print("Thank you for using the ATM")
                break
            else:
                print("Invalid choice")


class Account:
    def __init__(self, user_id, name, pin):
        self.user_id = user_id
        self.name = name
        self.pin = pin
        self.balance = 0
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"{datetime.datetime.now()} - Deposited Rs.{amount}")
        logging.info(f"Deposit: {self.user_id}, Amount: {amount}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(f"{datetime.datetime.now()} - Withdrew Rs.{amount}")
            logging.info(f"Withdrawal: {self.user_id}, Amount: {amount}")
        else:
            print("Insufficient funds")

    def transfer(self, amount, recipient_account):
        if self.balance >= amount:
            self.balance -= amount
            recipient_account.balance += amount
            self.transaction_history.append(f"{datetime.datetime.now()} - Transferred Rs.{amount} to {recipient_account.user_id}")
            recipient_account.transaction_history.append(f"{datetime.datetime.now()} - Received Rs.{amount} from {self.user_id}")
            logging.info(f"Transfer: From {self.user_id} to {recipient_account.user_id}, Amount: {amount}")
        else:
            print("Insufficient funds")

    def display_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    def check_pin(self, pin_attempt):
        return self.pin == pin_attempt

    def change_pin(self, new_pin):
        self.pin = new_pin
        logging.info(f"PIN changed: {self.user_id}")


if __name__ == "__main__":
    atm = ATM()
    atm.create_account()
    atm.create_account()
    atm.start()
