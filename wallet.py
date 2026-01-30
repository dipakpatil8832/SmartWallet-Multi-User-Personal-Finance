from datetime import datetime
from database import get_connection

class Wallet:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0.0
        self._load_balance()

    def _load_balance(self):
        conn = get_connection()
        cur = conn.cursor()

        # ✅ USER-SPECIFIC BALANCE
        cur.execute("""
            SELECT balance FROM transactions
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 1
        """, (self.user_id,))

        row = cur.fetchone()
        self.balance = float(row[0]) if row else 0.0

        conn.close()

    def add_balance(self, amount, note):
        self.balance += amount
        self._save("ADD", note, amount)

    def spend(self, amount, reason):
        if amount > self.balance:
            return False
        self.balance -= amount
        self._save("SPEND", reason, amount)
        return True

    def _save(self, ttype, note, amount):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO transactions
            (user_id, date, type, note, amount, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.user_id,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
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

        # ✅ USER-SPECIFIC TRANSACTIONS
        cur.execute("""
            SELECT date, type, note, amount, balance
            FROM transactions
            WHERE user_id=?
            ORDER BY id DESC
        """, (self.user_id,))

        rows = cur.fetchall()
        conn.close()

        return [
            {
                "date": datetime.strptime(r[0], "%Y-%m-%d %H:%M"),
                "type": r[1],
                "note": r[2],
                "amount": r[3],
                "balance": r[4]
            }
            for r in rows
        ]
