from flask import Flask, render_template, request, redirect, url_for, flash
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'

expenses = []
budget = None

@app.route('/')
def index():
    total = sum(expense['amount'] for expense in expenses)
    over_budget = budget is not None and total > budget
    return render_template('index.html', expenses=expenses, total=total, budget=budget, over_budget=over_budget)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        global budget
        description = request.form['description']
        amount = float(request.form['amount'])
        date = request.form['date']
        if budget is not None and sum(expense['amount'] for expense in expenses) + amount > budget:
            flash('Warning: Adding this expense will exceed your budget.', 'warning')
            return redirect(url_for('add_expense'))
        expenses.append({'description': description, 'amount': amount, 'date': date})
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    global budget
    if request.method == 'POST':
        budget = float(request.form['budget'])
        return redirect(url_for('index'))
    return render_template('set_budget.html')

@app.route('/plot')
def plot():
    expense_dict = defaultdict(list)
    for expense in expenses:
        expense_dict[expense['date']].append(expense['amount'])

    dates = list(expense_dict.keys())
    amounts = [sum(amounts) for amounts in expense_dict.values()]

    plt.figure(figsize=(10, 5))  # Set figure size
    plt.plot(dates, amounts, color='#1f77b4', linewidth=2)  # Set line color and width
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Amount (₹)', fontsize=14)
    plt.title('Expense Over Time', fontsize=20)
    plt.grid(True, linestyle='--', linewidth=0.5)  # Add grid with dashed lines
    plt.xticks(rotation=45)  # Rotate x-axis labels
    plt.tight_layout()  # Adjust spacing between plot and axes
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return render_template('plot.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
