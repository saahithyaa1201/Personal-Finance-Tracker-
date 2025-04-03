import json
from datetime import datetime
from GUI import main

# Global dictionary to store transactions
transactions = {}

# File handling functions
def load_transactions():
    global transactions
    try:
        with open('transactions.json', 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = {}

def save_transactions():
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)

def read_bulk_transactions_from_file(filename):
    global transactions
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(',')
                if len(data) == 3:
                    category, amount, date = data
                    transaction = {"amount": float(amount), "date": date}
                    if category not in transactions:
                        transactions[category] = [transaction]
                    else:
                        transactions[category].append(transaction)
    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    save_transactions()

# Feature implementations

def add_transaction():
    global transactions
    
    amount = float(input("Enter the transaction amount: "))
    category = input("Enter the category: ")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    while True:
        next_amount = input("Enter the transaction amount or type 'done' to finish: ")
        if next_amount.lower() == 'done':
            break
        next_amount = float(next_amount)
        trans = {"amount": next_amount, "date": current_date}
        
        # Check if the category already exists in transactions
        if category in transactions:
            transactions[category].append(trans)
        else:
            transactions[category] = [trans]

    save_transactions()
    print("Transaction has been added successfully!")


def view_transactions():
    global transactions
    if not transactions:
        print("There are no transactions to display")
    else:
        for category, transaction_list in transactions.items():
            print(f"Category: {category}")
            for transaction in transaction_list:
                print(f"\tAmount: {transaction['amount']},  Date: {transaction['date']}")
            print()

def update_transaction():
    view_transactions()
    if not transactions:
        print("No transactions to update")
        return
    category = input("Enter the category of the transaction to update: ")
    if category not in transactions:
        print("Category not found.")
        return
    index = int(input("Enter the index of the transaction to update: "))
    if index <= 0 or index > len(transactions[category]):
        print("Invalid index")
        return
    new_amount = float(input("Enter updated transaction amount: "))
    transactions[category][index - 1]["amount"] = new_amount
    save_transactions()
    print("Transaction updated successfully")

def delete_transaction():
    view_transactions()
    if not transactions:
        print("No transactions to delete")
        return
    category = input("Enter the category of the transaction to delete: ")
    if category not in transactions:
        print("Category not found.")
        return
    index = int(input("Enter the index of the transaction to delete: "))
    if index <= 0 or index > len(transactions[category]):
        print("Invalid index")
        return
    del transactions[category][index - 1]
    if not transactions[category]:
        del transactions[category]
    save_transactions()
    print("Transaction deleted successfully")

def display_summary():
    total_expense = sum(sum(transaction['amount'] for transaction in transaction_list) for transaction_list in transactions.values())
    print("Total Expenses:", total_expense)

def main_menu():
    load_transactions()
    while True:
        print("\nMain Menu:")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Read Bulk Transactions from File")
        print("7.GUI display")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            transactions = add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            filename = input("Enter the filename to read bulk transactions from: ")
            read_bulk_transactions_from_file(filename)
        elif choice == "7":
            main()
        elif choice == "8":
            save_transactions()
            break
        else:
            print("You chose an invalid option. Please try again.")

    print("Exiting...")

#main_menu() 
if __name__ == "__main__":
    main_menu()                                                                             
