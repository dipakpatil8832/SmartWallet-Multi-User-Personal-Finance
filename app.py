from flask import Flask, get_flashed_messages, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection ,create_tables
from wallet import Wallet
from flask import flash
import os


app = Flask(__name__)
app.secret_key = "super-secret-key"

create_tables()   


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            return redirect("/home")
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")
from werkzeug.security import check_password_hash


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


    
@app.route("/")
def root():
    if "user_id" in session:
        return redirect("/home")
    return redirect("/login")

@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect("/login")

    wallet = Wallet(session["user_id"])
    return render_template(
        "index.html",
        balance=wallet.balance,
        username=session.get("username")
    )


@app.route("/add_balance", methods=["GET", "POST"])
def add_balance():
    if "user_id" not in session:
        return redirect("/login")

    wallet = Wallet(session["user_id"])

    if request.method == "POST":
        wallet.add_balance(float(request.form["amount"]), request.form["note"])
        return redirect("/")

    return render_template("add_balance.html")


@app.route("/expense", methods=["GET", "POST"])
def expense():
    if "user_id" not in session:
        return redirect("/login")

    wallet = Wallet(session["user_id"])

    if request.method == "POST":
        wallet.spend(float(request.form["amount"]), request.form["reason"])
        return redirect("/")

    return render_template("expense.html")

@app.route("/passbook")
def passbook():
    if "user_id" not in session:
        return redirect("/login")

    wallet = Wallet(session["user_id"])
    return render_template(
        "passbook.html",
        transactions=wallet.get_transactions(),
        balance=wallet.balance
    )
@app.route("/monthly", methods=["GET", "POST"])
def monthly():
    if "user_id" not in session:
        return redirect("/login")

    wallet = Wallet(session["user_id"])
    report = None

    if request.method == "POST":
        month = int(request.form["month"])
        year = int(request.form["year"])

        credit = debit = 0
        rows = []

        for t in wallet.get_transactions():
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

from werkzeug.security import generate_password_hash
from flask import request, redirect, render_template

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        get_flashed_messages()
    if request.method == "POST":
        username = request.form["username"]
        password_raw = request.form["password"]
        
        
        if len(password_raw) < 6:
            flash("Password must be at least 6 characters", "error")
            return redirect("/register")

        conn = get_connection()
        cur = conn.cursor()

        
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            conn.close()
            flash("Username already exists. Please choose another.", "error")
            return redirect("/register")

        
        password = generate_password_hash(password_raw)

        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        flash("Account created successfully. Please login.", "success")
        return redirect("/login")

    return render_template("register.html")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
