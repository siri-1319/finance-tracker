# Smart Personal Finance Tracker

A command-line personal finance management application built with Python and SQLite. Track income and expenses, set category-wise budgets, get bill reminders, view spending reports, and visualize your financial data — all from the terminal.

## Features

- **Transaction Management**: Add, view, and track income/expense transactions
- **Category-wise Analysis**: View total spending/income grouped by category
- **Budget Tracking**: Set monthly budget limits per category and get over-budget alerts
- **Bill Reminders**: Track upcoming bills sorted by due date using a min-heap
- **Top Expenses**: Identify your biggest expenses using heap-based sorting
- **Date-Range Reports**: Filter transactions between any two dates
- **Recurring Transactions**: Set up recurring transactions (e.g., monthly rent, salary) processed via a queue
- **Data Visualization**: Pie chart for spending by category, bar chart for monthly trends

## Tech Stack

- **Language**: Python 3
- **Database**: SQLite
- **Visualization**: Matplotlib
- **Data Structures Used**:
  - Hash Maps (dict) — category-wise aggregation
  - Min-Heap (heapq) — bill reminders and top expenses
  - Queue (deque) — recurring transaction processing
  - SQL-based date range queries — sorted/filtered reporting

## Installation

1. Clone the repository:git clone https://github.com/siri-1319/finance-tracker.git

cd finance-tracker
2. Install dependencies:pip install -r requirements.txt
3. Run the application:python main.py
## Usage

On running the program, you'll see a menu with options:
1. Add Transaction
2. View All Transactions
3. Show Total Balance
4. Show Totals by Category
5. Set Budget
6. Check Budget Status
7. Add Bill
8. Show Upcoming Bills
9. Show Top 3 Biggest Expenses
10. Show Transactions by Date Range
11. Add Recurring Transaction
12. Process Recurring Transactions
13. Show Spending Pie Chart
14. Show Monthly Trend Bar Chart
15. Exit
Simply enter the number corresponding to the action you want to perform.

## Web Application (Flask)

In addition to the CLI version, this project includes a web-based interface built with Flask.

### Running the web app
python app.py

Then open your browser and go to:
http://127.0.0.1:5000

### Web Features

- **Home page**: View all transactions and add new ones via a form
- **Budget page** (`/budget`): Set category budgets and view spending vs. budget status
- **Charts page** (`/charts`): View pie chart (spending by category) and bar chart (monthly net totals)

## Project Structure
finance-tracker/

├── main.py          # CLI menu and application logic

├── database.py      # Database operations (SQLite)

├── requirements.txt # Python dependencies

└── README.md
## Future Improvements

- Web-based dashboard using Flask
- User authentication for multi-user support
- Export reports to PDF/CSV
- Email/SMS alerts for budget overruns and bill due dates

## Author

Siri ([@siri-1319](https://github.com/siri-1319))