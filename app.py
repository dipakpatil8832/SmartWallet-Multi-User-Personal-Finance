from flask import Flask, render_template, request, redirect
from wallet import Wallet
from datetime import datetime
from database import create_tables
import os
create_tables()
wallet = Wallet(500)


app = Flask(__name__)
wallet = Wallet(500)

# HOME
@app.route("/")
def index():
    return render_template("index.html", balance=wallet.balance)

# ADD BALANCE
@app.route("/add_balance", methods=["GET", "POST"])
def add_balance():
    if request.method == "POST":
        amount = float(request.form["amount"])
        note = request.form["note"]
        wallet.add_balance(amount, note, datetime.now())
        return redirect("/")
    return render_template("add_balance.html")

# ADD EXPENSE
@app.route("/expense", methods=["GET", "POST"])
def expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        reason = request.form["reason"]
        wallet.spend(amount, reason, datetime.now())
        return redirect("/")
    return render_template("expense.html")

# PASSBOOK
@app.route("/passbook")
def passbook():
    return render_template(
        "passbook.html",
        transactions=wallet.get_transactions(),
        balance=wallet.balance
    )


# MONTHLY REPORT
@app.route("/monthly", methods=["GET", "POST"])
def monthly():
    report = None

    if request.method == "POST":
        month = int(request.form["month"])
        year = int(request.form["year"])

        credit = 0
        debit = 0
        rows = []
        transactions = wallet.get_transactions()

        for t in transactions:
            if t["date"].month == month and t["date"].year == year:
                if t["type"] == "ADD":
                    credit += t["amount"]
                else:
                    debit += t["amount"]
                rows.append(t)

        report = {
            "credit": credit,
            "debit": debit,
            "saving": credit - debit,
            "rows": rows,
            "month": month,
            "year": year
        }

    return render_template("monthly.html", report=report)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)