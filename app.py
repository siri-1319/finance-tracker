from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)


@app.route('/')
def home():
    """Homepage - shows all transactions"""
    transactions = database.get_all_transactions()
    return render_template('index.html', transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    """Handle form submission to add a new transaction"""
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']
    
    database.add_transaction(date, category, amount, description)
    return redirect(url_for('home'))
if __name__ == '__main__':
    database.create_table()
    database.create_budget_table()
    database.create_bills_table()
    database.create_recurring_table()
    app.run(debug=True)