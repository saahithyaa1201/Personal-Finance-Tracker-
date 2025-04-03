#import json file
import json
#import tkinter as tk
import tkinter as tk
#imports the themed widget set ttk
from tkinter import ttk

#initialize with master parameter
class PersonalFinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        #sets the title of the window
        self.root.title("Personal Finance Tracker")

        # Create a colored title label
        title_label = tk.Label(self.root, text="Personal Finance Tracker", font=("Helvetica", 16, "bold"), fg="blue")
        title_label.grid(row=0, column=0, columnspan=3, pady=10)  # Place the label at row 0

        #loads transactions from JSON file
        self.load_transactions()
        #Create Gui widgets
        self.create_widgets()
        self.display_transactions()
    
    def load_transactions(self):
        try:
            #if the file found it reads its content
            with open('transactions.json', 'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = {}

    #Creating and configuring GUI widgets for the personal tracker
    def create_widgets(self):
        #Creates an Entry widget which allows users to input text
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=1, column=1)
        
        #Create a Button widget labeled search
        self.search_button = tk.Button(self.root, text="Search", command=self.search_transactions)
        self.search_button.grid(row=1, column=2)
        
        #Create Treeview widget to display transaction data in tabular format with columns for category, Amount, Date
        self.transaction_tree = ttk.Treeview(self.root, columns=("Category", "Amount", "Date"))
        self.transaction_tree.grid(row=2, column=0, columnspan=3, sticky="nsew")

        #Sets heading for each column in the Treeview widget
        self.transaction_tree.heading("#0", text="ID")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Date", text="Date")

        #Configures the width of each column in the Treeview widget
        self.transaction_tree.column("#0", width=100)
        self.transaction_tree.column("Category", width=200)
        self.transaction_tree.column("Amount", width=100)
        self.transaction_tree.column("Date", width=100)

        #Create a button labeled with load transaction and this button triggers the display_transactions
        self.load_button = tk.Button(self.root, text="Load Transactions", command=self.display_transactions)
        self.load_button.grid(row=3, column=0)

        #Clicking this Button triggers the sort_transactions method and placed in row 3 column 1
        self.sort_button = tk.Button(self.root, text="Sort by Date", command=self.sort_transactions)
        self.sort_button.grid(row=3, column=1)

    def display_transactions(self):
        #clears all the existing items(rows) in widget and children nodes
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        current_id = 1 
        for category, transaction_list in self.transactions.items():
            for transaction in transaction_list:
                self.transaction_tree.insert("", "end", text=current_id, values=(category, transaction["amount"], transaction["date"]))
                current_id += 1  # Increment the ID counter after each insertion

    def search_transactions(self):
        query = self.search_entry.get().lower()
        if query:
            filtered_transactions = {}
            for category, transactions in self.transactions.items():
                filtered_transactions[category] = []
                if query in category.lower():
                    filtered_transactions[category].extend(transactions)
                else:
                    filtered_transactions[category] = [transaction for transaction in transactions if query in str(transaction.values()).lower()]
            self.display_filtered_transactions(filtered_transactions)
        else:
            self.display_transactions()

    def display_filtered_transactions(self, filtered_transactions):
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        for i, (category, transaction_list) in enumerate(filtered_transactions.items(), start=1):
            for transaction in transaction_list:
                self.transaction_tree.insert("", "end", text=i, values=(category, transaction["amount"], transaction["date"]))

    def sort_transactions(self):
        sorted_transactions = {category: sorted(transactions, key=lambda x: x["date"]) for category, transactions in self.transactions.items()}
        self.display_sorted_transactions(sorted_transactions)

    def display_sorted_transactions(self, sorted_transactions):
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        for i, (category, transaction_list) in enumerate(sorted_transactions.items(), start=1):
            for transaction in transaction_list:
                self.transaction_tree.insert("", "end", text=i, values=(category, transaction["amount"], transaction["date"]))

def main():
    root = tk.Tk()
    app = PersonalFinanceTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()  
