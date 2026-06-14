from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)


@app.route('/')
def home():
    """Homepage - shows all transactions"""
    transactions = database.get_all_transactions()
    return render_template('index.html', transactions=transactions)


if __name__ == '__main__':
    database.create_table()
    database.create_budget_table()
    database.create_bills_table()
    database.create_recurring_table()
    app.run(debug=True)