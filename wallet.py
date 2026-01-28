from datetime import datetime
from database import get_connection

class Wallet:
    def __init__(self, opening_balance=0):
        self.balance = opening_balance
        self._load_balance()

    def _load_balance(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM transactions ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        if row:
            self.balance = row[0]
        conn.close()

    def add_balance(self, amount, note, dt=None):
        if dt is None:
            dt = datetime.now()

        self.balance += amount
        self._save_transaction(dt, "ADD", note, amount)

    def spend(self, amount, reason, dt=None):
        if amount > self.balance:
            return False

        if dt is None:
            dt = datetime.now()

        self.balance -= amount
        self._save_transaction(dt, "SPEND", reason, amount)
        return True

    def _save_transaction(self, dt, ttype, note, amount):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO transactions (date, type, note, amount, balance)
        VALUES (?, ?, ?, ?, ?)
        """, (
            dt.strftime("%Y-%m-%d %H:%M"),
            ttype,
            note,
            amount,
            self.balance
        ))

        conn.commit()
        conn.close()

    def get_transactions(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT date, type, note, amount, balance FROM transactions ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "date": datetime.strptime(r[0], "%Y-%m-%d %H:%M"),
                "type": r[1],
                "note": r[2],
                "amount": r[3],
                "balance": r[4]
            })
        return result
