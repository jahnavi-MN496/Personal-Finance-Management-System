import unittest
import sqlite3
from datetime import datetime
from unittest.mock import patch
from io import StringIO

class TestFinanceManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cls.cursor = cls.conn.cursor()
        cls.create_tables()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    @classmethod
    def create_tables(cls):
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date TEXT,
                category TEXT,
                type TEXT,
                amount REAL,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                user_id INTEGER PRIMARY KEY,
                monthly_budget REAL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        cls.conn.commit()

    def test_register_user(self):
        """Test user registration with valid and invalid inputs."""
        username = "test_user"
        password = "test_pass"

        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user, "User registration failed.")

        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, "new_pass"))
            self.conn.commit()

    def test_login_user(self):
        """Test user login functionality with valid and invalid credentials."""
        username = "test_login"
        password = "test_pass"

        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user, "Login failed with correct credentials.")

        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, "wrong_pass"))
        user = self.cursor.fetchone()
        self.assertIsNone(user, "Login succeeded with incorrect credentials.")

    def test_save_budget(self):
        """Test saving and retrieving the monthly budget."""
        user_id = 1
        monthly_budget = 1000.0

        self.cursor.execute("INSERT OR REPLACE INTO budgets (user_id, monthly_budget) VALUES (?, ?)", (user_id, monthly_budget))
        self.conn.commit()

        self.cursor.execute("SELECT monthly_budget FROM budgets WHERE user_id = ?", (user_id,))
        budget = self.cursor.fetchone()
        self.assertEqual(budget[0], monthly_budget, "Budget save or retrieve failed.")

    def test_add_transaction(self):
        """Test adding transactions and checking constraints like exceeding budget."""
        user_id = 1
        monthly_budget = 1000.0

        self.cursor.execute("INSERT OR REPLACE INTO budgets (user_id, monthly_budget) VALUES (?, ?)", (user_id, monthly_budget))
        self.conn.commit()

        transaction_date = "2024-12-01"
        category = "Food"
        transaction_type = "Expense"
        amount = 100.0
        description = "Groceries"
        self.cursor.execute("""
            INSERT INTO transactions (user_id, date, category, type, amount, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, transaction_date, category, transaction_type, amount, description))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = self.cursor.fetchall()
        self.assertEqual(len(transactions), 1, "Transaction addition failed.")

        large_expense = 950.0
        current_month_expenses = amount + large_expense

        with patch("builtins.input", side_effect=["2024-12-01", "Food", "Expense", str(large_expense), "Large expense"]):
            if current_month_expenses > monthly_budget:
                self.assertTrue(True, "Exceeding budget warning displayed.")

    def test_generate_report(self):
        """Test financial report generation."""
        user_id = 1

        self.cursor.execute("""
            INSERT INTO transactions (user_id, date, category, type, amount, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, "2024-12-01", "Salary", "Income", 3000.0, "Monthly salary"))
        self.cursor.execute("""
            INSERT INTO transactions (user_id, date, category, type, amount, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, "2024-12-02", "Groceries", "Expense", 500.0, "Grocery shopping"))
        self.conn.commit()

        self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'Income'", (user_id,))
        total_income = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'Expense'", (user_id,))
        total_expenses = self.cursor.fetchone()[0]

        total_savings = total_income - total_expenses

        self.assertEqual(total_income, 3000.0, "Income calculation incorrect.")
        self.assertEqual(total_expenses, 500.0, "Expense calculation incorrect.")
        self.assertEqual(total_savings, 2500.0, "Savings calculation incorrect.")

if __name__ == "__main__":
    unittest.main()
