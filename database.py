import sqlite3

DB_NAME = "finance.db"

def create_table():
    """Create the transactions table if it doesn't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database and table ready!")
def create_budget_table():
    """Create the budgets table if it doesn't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            limit_amount REAL
        )
    """)
    
    conn.commit()
    conn.close()
def create_bills_table():
    """Create table for recurring/upcoming bills"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            due_date TEXT,
            amount REAL
        )
    """)
    
    conn.commit()
    conn.close()
def add_transaction(date, category, amount, description):
    """Insert a new transaction into the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO transactions (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """, (date, category, amount, description))
    
    conn.commit()
    conn.close()

def get_all_transactions():
    """Fetch all transactions from the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    
    conn.close()
    return rows
def set_budget(category, limit_amount):
    """Set or update a budget limit for a category"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO budgets (category, limit_amount)
        VALUES (?, ?)
        ON CONFLICT(category) DO UPDATE SET limit_amount = ?
    """, (category, limit_amount, limit_amount))
    
    conn.commit()
    conn.close()


def get_all_budgets():
    """Fetch all budgets"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM budgets")
    rows = cursor.fetchall()
    
    conn.close()
    return rows
# This runs only if you run database.py directly (for testing)
def add_bill(name, due_date, amount):
    """Add a recurring bill"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO bills (name, due_date, amount)
        VALUES (?, ?, ?)
    """, (name, due_date, amount))
    
    conn.commit()
    conn.close()


def get_all_bills():
    """Fetch all bills"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM bills")
    rows = cursor.fetchall()
    
    conn.close()
    return rows
if __name__ == "__main__":
    create_table()
    create_budget_table()
    create_bills_table()