from flask import Flask, render_template, request, redirect
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

expense_list_global = []
count = 0

class Expense:
    def __init__(self, num, title, amount):
        self.id = num
        self.title = title
        self.amount = amount

@app.route("/")
def index():
    global expense_list_global
    return render_template("index.html", expense_list=expense_list_global)

@app.route("/add", methods=["POST"])
def add():
    global expense_list_global
    global count
    count += 1

    title = request.form.get("title")
    amount = request.form.get("amount")

    new_expense = Expense(num=count, title=title, amount=amount)
    expense_list_global.append(new_expense)
    for i, expense in enumerate(expense_list_global, start=1):
        expense.id = i
    return redirect("/")
    
    return redirect("/")

@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    global expense_list_global
    expense_list_global = [expense for expense in expense_list_global if expense.id != expense_id]
    for i, expense in enumerate(expense_list_global, start=1):
        expense.id = i
    return redirect("/")

@app.route("/plot")
def plot():
    global expense_list_global
    title = [expense.title for expense in expense_list_global]
    amounts = [float(expense.amount) for expense in expense_list_global]

    plt.bar(title, amounts)
    plt.xlabel("Title")
    plt.ylabel("Expense Amount")
    plt.title("Expense Tracker")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the plot image as base64
    plot_data = base64.b64encode(img.getvalue()).decode()

    plt.close()  # Close the plot to free up memory

    # Return the plot image data
    return f'<img src="data:image/png;base64,{plot_data}">'

if __name__ == "__main__":
    app.run(debug=True)
