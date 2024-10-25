import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                expense_name TEXT,
                amount REAL,
                expense_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        self.conn.commit()

    def insert_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def validate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone()

    def insert_expense(self, user_id, expense_name, amount, expense_date):
        self.cursor.execute("INSERT INTO expenses (user_id, expense_name, amount, expense_date) VALUES (?, ?, ?, ?)",
                            (user_id, expense_name, amount, expense_date))
        self.conn.commit()

    def get_expenses(self, user_id):
        self.cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def update_expense(self, expense_id, expense_name, amount, expense_date):
        self.cursor.execute("UPDATE expenses SET expense_name = ?, amount = ?, expense_date = ? WHERE expense_id = ?",
                            (expense_name, amount, expense_date, expense_id))
        self.conn.commit()

    def delete_expense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        self.conn.commit()
