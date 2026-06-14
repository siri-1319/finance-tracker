import matplotlib
matplotlib.use('Agg')  # needed for Flask (no GUI popup)
import matplotlib.pyplot as plt
import io
import base64
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
@app.route('/budget')
def budget_status():
    """Show budget vs spending"""
    budgets = database.get_all_budgets()
    transactions = database.get_all_transactions()
    
    spending = {}
    for row in transactions:
        category = row[2]
        amount = row[3]
        if amount < 0:
            spending[category] = spending.get(category, 0) + abs(amount)
    
    budget_data = []
    for category, limit_amount in budgets:
        spent = spending.get(category, 0)
        remaining = limit_amount - spent
        status = "OVER BUDGET" if spent > limit_amount else "OK"
        budget_data.append({
            'category': category,
            'spent': spent,
            'limit': limit_amount,
            'remaining': remaining,
            'status': status
        })
    
    return render_template('budget.html', budget_data=budget_data)


@app.route('/set_budget', methods=['POST'])
def set_budget():
    """Handle setting a budget"""
    category = request.form['category']
    limit_amount = float(request.form['limit_amount'])
    database.set_budget(category, limit_amount)
    return redirect(url_for('budget_status'))
if __name__ == '__main__':
    database.create_table()
    database.create_budget_table()
    database.create_bills_table()
    database.create_recurring_table()
    app.run(debug=True)