# main.py
from collections import deque
import heapq
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
def add_bill():
    """Ask user for bill details and save to database"""
    name = input("Enter bill name (e.g., Electricity): ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    amount = float(input("Enter amount: "))
    
    database.add_bill(name, due_date, amount)
    print(f"Bill added: {name} due on {due_date}\n")


def show_upcoming_bills():
    """Show bills sorted by due date using a min-heap"""
    bills = database.get_all_bills()
    
    if not bills:
        print("No bills found.\n")
        return
    
    # Build a min-heap based on due_date
    heap = []
    for bill in bills:
        # bill = (id, name, due_date, amount)
        heapq.heappush(heap, (bill[2], bill[1], bill[3]))  # (due_date, name, amount)
    
    print("\n--- Upcoming Bills (earliest first) ---")
    while heap:
        due_date, name, amount = heapq.heappop(heap)
        print(f"{name}: Due {due_date} -> Amount: {amount}")
    print()


def show_top_expenses(n=3):
    """Show top N biggest expenses using a max-heap (via negation)"""
    transactions = database.get_all_transactions()
    
    expenses = []
    for row in transactions:
        amount = row[3]
        if amount < 0:  # only expenses
            heapq.heappush(expenses, (amount, row))  # smallest (most negative) first = heapq is min-heap
    
    print(f"\n--- Top {n} Biggest Expenses ---")
    count = 0
    while expenses and count < n:
        amount, row = heapq.heappop(expenses)
        print(f"Date: {row[1]} | Category: {row[2]} | Amount: {amount} | Description: {row[4]}")
        count += 1
    print()
def show_date_range_report():
    """Show transactions between two dates"""
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    rows = database.get_transactions_by_date_range(start_date, end_date)
    
    if not rows:
        print("No transactions found in this date range.\n")
        return
    
    print(f"\n--- Transactions from {start_date} to {end_date} ---")
    total = 0
    for row in rows:
        print(f"Date: {row[1]} | Category: {row[2]} | Amount: {row[3]} | Description: {row[4]}")
        total += row[3]
    print(f"\nNet total for this period: {total}\n")
def add_recurring():
    """Add a recurring transaction template"""
    category = input("Enter category: ")
    amount = float(input("Enter amount (negative for expense, positive for income): "))
    description = input("Enter description: ")
    frequency = input("Enter frequency (e.g., Monthly): ")
    
    database.add_recurring(category, amount, description, frequency)
    print(f"Recurring transaction added: {category} ({frequency})\n")


def process_recurring():
    """Process all recurring transactions using a queue (FIFO)"""
    recurring_items = database.get_all_recurring()
    
    if not recurring_items:
        print("No recurring transactions set up.\n")
        return
    
    # Build a queue
    queue = deque(recurring_items)
    
    date = input("Enter date to apply these transactions (YYYY-MM-DD): ")
    
    print("\n--- Processing Recurring Transactions ---")
    while queue:
        item = queue.popleft()  # FIFO: process oldest-added first
        # item = (id, category, amount, description, frequency)
        category = item[1]
        amount = item[2]
        description = item[3]
        
        database.add_transaction(date, category, amount, description)
        print(f"Processed: {category} -> {amount} ({description})")
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
        print("7. Add Bill")
        print("8. Show Upcoming Bills (sorted by due date)")
        print("9. Show Top 3 Biggest Expenses")
        print("10. Show Transactions by Date Range")
        print("11. Add Recurring Transaction")
        print("12. Process Recurring Transactions")
        print("13. Exit")
        choice = input("Enter your choice (1-13): ")
        
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
            add_bill()
        elif choice == '8':
            show_upcoming_bills()
        elif choice == '9':
            show_top_expenses()
        elif choice == '10':
            show_date_range_report()
        elif choice == '11':
            add_recurring()
        elif choice == '12':
            process_recurring()
        elif choice == '13':
            print("Goodbye!")
            break

# This runs the program
if __name__ == "__main__":
    database.create_table()
    main_menu()