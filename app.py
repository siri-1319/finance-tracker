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
@app.route('/charts')
def charts():
    """Show pie and bar charts"""
    transactions = database.get_all_transactions()
    
    # Pie chart - spending by category
    category_totals = {}
    for row in transactions:
        category = row[2]
        amount = row[3]
        if amount < 0:
            category_totals[category] = category_totals.get(category, 0) + abs(amount)
    
    pie_url = None
    if category_totals:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
        ax.set_title("Spending by Category")
        pie_url = fig_to_base64(fig)
        plt.close(fig)
    
    # Bar chart - monthly net total
    monthly_totals = {}
    for row in transactions:
        date = row[1]
        amount = row[3]
        month = date[:7]
        monthly_totals[month] = monthly_totals.get(month, 0) + amount
    
    bar_url = None
    if monthly_totals:
        months = sorted(monthly_totals.keys())
        totals = [monthly_totals[m] for m in months]
        
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(months, totals, color='skyblue')
        ax.set_title("Monthly Net Total")
        ax.axhline(0, color='black', linewidth=0.8)
        bar_url = fig_to_base64(fig)
        plt.close(fig)
    
    return render_template('charts.html', pie_url=pie_url, bar_url=bar_url)


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_base64
if __name__ == '__main__':
    database.create_table()
    database.create_budget_table()
    database.create_bills_table()
    database.create_recurring_table()
    app.run(debug=True)