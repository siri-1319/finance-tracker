# main.py

# This list will store all our transactions temporarily (in memory)
transactions = []

def add_transaction():
    """Ask user for transaction details and add to the list"""
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g., Food, Salary, Rent): ")
    amount = float(input("Enter amount (use negative for expense, positive for income): "))
    description = input("Enter description: ")
    
    transaction = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }
    
    transactions.append(transaction)
    print("Transaction added successfully!\n")


def view_all_transactions():
    """Display all transactions"""
    if not transactions:
        print("No transactions found.\n")
        return
    
    print("\n--- All Transactions ---")
    for t in transactions:
        print(f"Date: {t['date']} | Category: {t['category']} | Amount: {t['amount']} | Description: {t['description']}")
    print()


def total_balance():
    """Calculate and show total balance"""
    total = sum(t['amount'] for t in transactions)
    print(f"\nTotal Balance: {total}\n")


def total_by_category():
    """Show total spending/income grouped by category"""
    category_totals = {}  # this is a dictionary (hash map)
    
    for t in transactions:
        cat = t['category']
        amount = t['amount']
        
        if cat in category_totals:
            category_totals[cat] += amount
        else:
            category_totals[cat] = amount
    
    print("\n--- Totals by Category ---")
    for category, total in category_totals.items():
        print(f"{category}: {total}")
    print()


def main_menu():
    """Main loop showing menu options to user"""
    while True:
        print("===== Finance Tracker =====")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Show Total Balance")
        print("4. Show Totals by Category")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_all_transactions()
        elif choice == '3':
            total_balance()
        elif choice == '4':
            total_by_category()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


# This runs the program
if __name__ == "__main__":
    main_menu()