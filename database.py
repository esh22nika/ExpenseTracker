import sqlite3
from datetime import datetime, timedelta
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
    def create_tables(self):
        # Table for user goals
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                user_id INTEGER PRIMARY KEY,
                weekly_goal REAL,
                monthly_goal REAL
            )
        ''')
        
        # Table for expenses (assuming it doesn't already exist)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                expense_category TEXT,
                amount REAL,
                date TEXT
            )
        ''')
        
        self.conn.commit()
    def set_goals(self, user_id, weekly_goal, monthly_goal):
        # Insert or update goals for the user
        self.cursor.execute('''
            INSERT INTO goals (user_id, weekly_goal, monthly_goal) 
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET weekly_goal = ?, monthly_goal = ?
        ''', (user_id, weekly_goal, monthly_goal, weekly_goal, monthly_goal))
        
        self.conn.commit()

    def get_goals(self, user_id):
        # Fetch goals for the user
        self.cursor.execute('SELECT weekly_goal, monthly_goal FROM goals WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()
        return result if result else (None, None)

    def get_weekly_expenses(self, user_id):
        # Calculate expenses from the past 7 days
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE user_id = ? AND expense_date >= ?
        ''', (user_id, one_week_ago))
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0.0

    def get_monthly_expenses(self, user_id):
        # Calculate expenses from the past 30 days
        one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.cursor.execute('''
            SELECT SUM(amount) FROM expenses 
            WHERE user_id = ? AND expense_date >= ?
        ''', (user_id, one_month_ago))
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0.0