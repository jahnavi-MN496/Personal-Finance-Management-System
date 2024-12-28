import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            user_id INTEGER PRIMARY KEY,
            monthly_budget REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

# User authentication
def register_user():
    username = register_username_entry.get().strip()
    password = register_password_entry.get().strip()
    if not (username and password):
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful! Please log in.")
        switch_frame(register_frame, login_frame)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    conn.close()

def login_user():
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()
    if not (username and password):
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        global current_user_id
        current_user_id = user[0]
        messagebox.showinfo("Success", f"Welcome, {username}!")
        switch_frame(login_frame, transaction_frame)
        display_transactions()
        load_budget()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Budget handling
def save_budget():
    budget = budget_entry.get()
    if not budget:
        messagebox.showerror("Error", "Please enter a budget.")
        return

    try:
        budget = float(budget)
    except ValueError:
        messagebox.showerror("Error", "Budget must be a number!")
        return

    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO budgets (user_id, monthly_budget) VALUES (?, ?)", (current_user_id, budget))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Monthly budget set successfully!")

def load_budget():
    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT monthly_budget FROM budgets WHERE user_id = ?", (current_user_id,))
    budget = cursor.fetchone()
    conn.close()
    if budget:
        budget_entry.delete(0, tk.END)
        budget_entry.insert(0, f"{budget[0]:.2f}")

def add_transaction():
    date = transaction_date_entry.get()
    category = transaction_category_combobox.get()
    type_ = transaction_type_combobox.get()
    amount = transaction_amount_entry.get()
    description = transaction_description_entry.get("1.0", "end-1c")

    if not (date and category and type_ and amount):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")  # Validate date format
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid date format or amount! Use YYYY-MM-DD for date.")
        return

    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()

    if type_ == "Expense":
        cursor.execute("SELECT monthly_budget FROM budgets WHERE user_id = ?", (current_user_id,))
        budget = cursor.fetchone()
        if budget:
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'Expense' AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')", (current_user_id,))
            current_month_expenses = cursor.fetchone()[0] or 0
            if current_month_expenses + amount > budget[0]:
                messagebox.showwarning("Warning", "This expense exceeds your monthly budget!")

    cursor.execute("""
        INSERT INTO transactions (user_id, date, category, type, amount, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (current_user_id, date, category, type_, amount, description))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Transaction added successfully!")
    clear_transaction_fields()
    display_transactions()

def display_transactions():
    for item in transaction_tree.get_children():
        transaction_tree.delete(item)

    conn = sqlite3.connect("finance_manager.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, category, type, amount, description FROM transactions WHERE user_id = ?", (current_user_id,))
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        transaction_tree.insert("", "end", values=row)

def generate_report_page():
    if current_user_id is None:
        messagebox.showerror("Error", "User is not logged in. Please log in to generate a report.")
        return

    switch_frame(transaction_frame, report_frame)
    try:
        conn = sqlite3.connect("finance_manager.db")
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type='Income'", (current_user_id,))
        total_income = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type='Expense'", (current_user_id,))
        total_expenses = cursor.fetchone()[0] or 0

        total_savings = total_income - total_expenses
        report_text.delete("1.0", tk.END)
        report_message = (f"Financial Report\n\n"
                          f"Total Income: ${total_income:.2f}\n"
                          f"Total Expenses: ${total_expenses:.2f}\n"
                          f"Total Savings: ${total_savings:.2f}")
        report_text.insert(tk.END, report_message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while generating the report: {e}")
    finally:
        conn.close()

def switch_frame(current_frame, next_frame):
    if current_frame is not None:
        current_frame.pack_forget()
    next_frame.pack(fill="both", expand=True)

def clear_transaction_fields():
    transaction_date_entry.delete(0, tk.END)
    transaction_category_combobox.set("")
    transaction_type_combobox.set("")
    transaction_amount_entry.delete(0, tk.END)
    transaction_description_entry.delete("1.0", "end")

root = tk.Tk()
root.configure(bg = "pink")
root.title("Personal Finance Manager")
root.geometry("1000x700")

welcome_frame = tk.Frame(root)
welcome_label = tk.Label(welcome_frame, text="Welcome to Personal Finance Manager", font=("Arial", 34))
welcome_label.pack(pady=200)
welcome_login_button = tk.Button(welcome_frame, text="Login",width=15,height=3,bd=2,font=("Arial",12), command=lambda: switch_frame(welcome_frame, login_frame))
welcome_login_button.place(x=500,y=300)
welcome_register_button = tk.Button(welcome_frame, text="Register",width=15,height=3,bd=2,font=("Arial",12), command=lambda: switch_frame(welcome_frame, register_frame))
welcome_register_button.place(x=700,y=300)
welcome_frame.pack(fill="both", expand=True)

login_frame = tk.Frame(root)
login_username_heading = tk.Label(login_frame, text="Login Page",font=("Arial",34))
login_username_heading.place(x=600)
login_username_label = tk.Label(login_frame, text="Username",font=("Arial",12))
login_username_label.place(x=600,y=100)
login_username_entry = tk.Entry(login_frame)
login_username_entry.place(x=700,y=100)
login_password_label = tk.Label(login_frame, text="Password",font=("Arial",12))
login_password_label.place(x=600,y=150)
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.place(x=700,y=150)
login_button = tk.Button(login_frame, text="Login", command=login_user)
login_button.place(x=650,y=200)
login_back_button = tk.Button(login_frame, text="Back", command=lambda: switch_frame(login_frame, welcome_frame))
login_back_button.place(x=700,y=200)

register_frame = tk.Frame(root)
register_username_heading = tk.Label(register_frame, text="Register Page",font=("Arial",34))
register_username_heading.place(x=550)
register_username_label = tk.Label(register_frame, text="Username",font=("Arial",12))
register_username_label.place(x=600,y=100)
register_username_entry = tk.Entry(register_frame)
register_username_entry.place(x=700,y=100)
register_password_label = tk.Label(register_frame, text="Password",font=("Arial",12))
register_password_label.place(x=600,y=150)
register_password_entry = tk.Entry(register_frame, show="*")
register_password_entry.place(x=700,y=150)
register_button = tk.Button(register_frame, text="Register", command=register_user)
register_button.place(x=650,y=200)
register_back_button = tk.Button(register_frame, text="Back", command=lambda: switch_frame(register_frame, welcome_frame))
register_back_button.place(x=750,y=200)

transaction_frame = tk.Frame(root)
transaction_label = tk.Label(transaction_frame, text="Transaction Manager", font=("Arial", 24))
transaction_label.pack(pady=10)
transaction_input_frame = tk.Frame(transaction_frame)
transaction_input_frame.pack(pady=10)
transaction_date_label = tk.Label(transaction_input_frame, text="Date (YYYY-MM-DD)")
transaction_date_label.grid(row=0, column=0, padx=5, pady=5)
transaction_date_entry = tk.Entry(transaction_input_frame)
transaction_date_entry.grid(row=0, column=1, padx=5, pady=5)
transaction_category_label = tk.Label(transaction_input_frame, text="Category")
transaction_category_label.grid(row=1, column=0, padx=5, pady=5)
transaction_category_combobox = ttk.Combobox(transaction_input_frame, values=["Food", "Transport", "Shopping", "Utilities", "Others"])
transaction_category_combobox.grid(row=1, column=1, padx=5, pady=5)
transaction_type_label = tk.Label(transaction_input_frame, text="Type")
transaction_type_label.grid(row=2, column=0, padx=5, pady=5)
transaction_type_combobox = ttk.Combobox(transaction_input_frame, values=["Income", "Expense"])
transaction_type_combobox.grid(row=2, column=1, padx=5, pady=5)
transaction_amount_label = tk.Label(transaction_input_frame, text="Amount")
transaction_amount_label.grid(row=3, column=0, padx=5, pady=5)
transaction_amount_entry = tk.Entry(transaction_input_frame)
transaction_amount_entry.grid(row=3, column=1, padx=5, pady=5)
transaction_description_label = tk.Label(transaction_input_frame, text="Description")
transaction_description_label.grid(row=4, column=0, padx=5, pady=5)
transaction_description_entry = tk.Text(transaction_input_frame, height=4, width=30)
transaction_description_entry.grid(row=4, column=1, padx=5, pady=5)
transaction_add_button = tk.Button(transaction_input_frame, text="Add Transaction", command=add_transaction)
transaction_add_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")
report_button = tk.Button(transaction_input_frame, text="Generate Report", command=generate_report_page)
# report_button.pack(pady=0)
report_button.grid(row=5, column=0, padx=5, pady=5, sticky="e")

transaction_tree = ttk.Treeview(transaction_frame, columns=("ID", "Date", "Category", "Type", "Amount", "Description"), show="headings")
transaction_tree.heading("ID", text="ID")
transaction_tree.heading("Date", text="Date")
transaction_tree.heading("Category", text="Category")
transaction_tree.heading("Type", text="Type")
transaction_tree.heading("Amount", text="Amount")
transaction_tree.heading("Description", text="Description")
transaction_tree.pack(pady=20, fill="both", expand=True)
budget_label = tk.Label(transaction_frame, text="Monthly Budget")
budget_label.pack()
budget_entry = tk.Entry(transaction_frame)
budget_entry.pack(pady=5)
save_budget_button = tk.Button(transaction_frame, text="Save Budget", command=save_budget)
save_budget_button.pack(pady=5)

report_frame = tk.Frame(root)
report_text = tk.Text(report_frame, height=15, width=80)
report_text.pack(pady=20)
report_back_button = tk.Button(report_frame, text="Back", command=lambda: switch_frame(report_frame, transaction_frame))
report_back_button.pack()

setup_database()
switch_frame(welcome_frame, welcome_frame)
root.mainloop()
