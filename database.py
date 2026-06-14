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

# This runs only if you run database.py directly (for testing)
if __name__ == "__main__":
    create_table()