from wallet import Wallet
from datetime import datetime

print("💳 Welcome to Personal Wallet App")

opening_balance = float(input("Enter opening balance: ₹"))
wallet = Wallet(opening_balance)

def get_datetime_from_user():
    date_str = input("Enter date (DD-MM-YYYY) or press ENTER for today: ")
    time_str = input("Enter time (HH:MM) or press ENTER for now: ")

    if date_str == "" and time_str == "":
        return datetime.now()

    if time_str == "":
        time_str = "00:00"

    return datetime.strptime(date_str + " " + time_str, "%d-%m-%Y %H:%M")


while True:
    print("""
1. Add Balance
2. Add Expense
3. Show Balance
4. View Passbook
5. Monthly Report
6. Exit
""")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        amount = float(input("Enter amount to add: ₹"))
        note = input("Enter note (Salary, Gift): ")
        dt = get_datetime_from_user()
        wallet.add_balance(amount, note, dt)
        print("✅ Balance added")

    elif choice == "2":
        amount = float(input("Enter expense amount: ₹"))
        reason = input("Enter reason (Tea, Breakfast, Travel): ")
        dt = get_datetime_from_user()
        if wallet.spend(amount, reason, dt):
            print("✅ Expense recorded")

    elif choice == "3":
        print(f"\n💰 Current Balance: ₹{wallet.balance}")

    elif choice == "4":
        wallet.show_passbook()

    elif choice == "5":
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year (YYYY): "))
        wallet.monthly_report(month, year)

    elif choice == "6":
        print("👋 Thank you for using Wallet App")
        break

    else:
        print("❌ Invalid choice")
