# main.py

# This list will store all our transactions temporarily (in memory)
import database
def add_transaction():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g., Food, Salary, Rent): ")
    amount = float(input("Enter amount (use negative for expense, positive for income): "))
    description = input("Enter description: ")
    database.add_transaction(date, category, amount, description)
    print("Transaction added successfully!\n")


def view_all_transactions():
    """Display all transactions from database"""
    rows = database.get_all_transactions()
    
    if not rows:
        print("No transactions found.\n")
        return
    
    print("\n--- All Transactions ---")
    for row in rows:
        # row = (id, date, category, amount, description)
        print(f"ID: {row[0]} | Date: {row[1]} | Category: {row[2]} | Amount: {row[3]} | Description: {row[4]}")
    print()


def total_balance():
    """Calculate and show total balance"""
    rows = database.get_all_transactions()
    total = sum(row[3] for row in rows)  # row[3] is amount
    print(f"\nTotal Balance: {total}\n")

def total_by_category():
    """Show total spending/income grouped by category"""
    rows = database.get_all_transactions()
    category_totals = {}
    
    for row in rows:
        cat = row[2]      # category
        amount = row[3]   # amount
        
        if cat in category_totals:
            category_totals[cat] += amount
        else:
            category_totals[cat] = amount
    
    print("\n--- Totals by Category ---")
    for category, total in category_totals.items():
        print(f"{category}: {total}")
    print()
def set_budget():
    """Ask user for category and budget limit, save to database"""
    category = input("Enter category (e.g., Food, Rent, Entertainment): ")
    limit_amount = float(input("Enter budget limit for this category: "))
    
    database.set_budget(category, limit_amount)
    print(f"Budget set: {category} -> {limit_amount}\n")


def check_budget_status():
    """Compare spending vs budget for each category"""
    budgets = database.get_all_budgets()
    
    if not budgets:
        print("No budgets set yet.\n")
        return
    
    transactions = database.get_all_transactions()
    
    # Calculate spending per category (only expenses, i.e., negative amounts)
    spending = {}
    for row in transactions:
        category = row[2]
        amount = row[3]
        if amount < 0:  # expense
            spending[category] = spending.get(category, 0) + abs(amount)
    
    print("\n--- Budget Status ---")
    for category, limit_amount in budgets:
        spent = spending.get(category, 0)
        remaining = limit_amount - spent
        
        status = "OK"
        if spent > limit_amount:
            status = "OVER BUDGET!"
        
        print(f"{category}: Spent {spent} / Limit {limit_amount} -> {status} (Remaining: {remaining})")
    print()
def main_menu():
    """Main loop showing menu options to user"""
    while True:
        print("===== Finance Tracker =====")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Show Total Balance")
        print("4. Show Totals by Category")
        print("5. Set Budget")
        print("6. Check Budget Status")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_all_transactions()
        elif choice == '3':
            total_balance()
        elif choice == '4':
            total_by_category()
        elif choice == '5':
            set_budget()
        elif choice == '6':
            check_budget_status()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


# This runs the program
if __name__ == "__main__":
    database.create_table()
    main_menu()