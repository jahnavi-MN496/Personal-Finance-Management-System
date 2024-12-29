# Personal-Finance-Management-System 
________________________________________
Introduction
The Personal Finance Manager is a Python-based desktop application developed using Tkinter for the GUI and SQLite for data storage. The application allows users to:
1.	Register and log in.
2.	Manage budgets and track transactions.
3.	Generate financial reports (income, expenses, and savings).
________________________________________
Features
1.	User Authentication
o	Secure registration and login functionality.
o	Passwords are stored as plain text (for simplicity; for real-world applications, hashing is recommended).
2.	Budget Management
o	Users can set and update a monthly budget.
o	Budgets are user-specific and tracked independently.
3.	Transaction Management
o	Add transactions categorized as income or expenses.
o	Include details like date, category, amount, and description.
o	Warn users if expenses exceed the monthly budget.
4.	Report Generation
o	Summarize total income, expenses, and net savings.
o	Display financial reports directly in the application.
________________________________________
Installation Instructions
1.	Prerequisites
o	Python 3.x installed on your system.
o	Required Python libraries: tkinter, sqlite3, datetime.
2.	Setup
o	Save the script as finance_manager.py in a folder.
o	Run the script to initialize the database:  finance_manager.py
________________________________________
Usage Guide
Starting the Application
1.	Run the script:
bash
Copy code
python finance_manager.py
2.	Home Screen
o	Click on Login if you already have an account.
o	Click on Register to create a new account.
Registering a New User
1.	Enter a unique username and password.
2.	Click Register to create your account.
3.	Upon successful registration, log in using the same credentials.
Logging In
1.	Enter your username and password.
2.	Click Login to access the transaction management interface.
Setting Your Budget
1.	Enter your monthly budget in the input field under "Monthly Budget."
2.	Click Save Budget. A success message will confirm the update.
Adding Transactions
1.	Input the transaction details:
o	Date: Use the format YYYY-MM-DD.
o	Category: Select from predefined options like Food, Transport, etc.
o	Type: Choose between Income or Expense.
o	Amount: Enter a numeric value.
o	Description: Optionally, add details about the transaction.
2.	Click Add Transaction to save the transaction.
3.	If the transaction exceeds your monthly budget, a warning message is displayed.
Viewing Transactions
•	All transactions are displayed in a table format, showing:
o	Date, Category, Type, Amount, and Description.
Generating Reports
1.	Click on Generate Report to view a summary of:
o	Total income.
o	Total expenses.
o	Net savings.
Returning to the Main Menu
•	Click Back to navigate between pages.
________________________________________
Code Structure
1.	Database Setup
o	The setup_database() function creates three tables:
	users: Stores user credentials.
	transactions: Logs all transactions for users.
	budgets: Saves user-specific monthly budgets.
2.	Authentication Functions
o	register_user(): Handles user registration.
o	login_user(): Verifies login credentials and loads user data.
3.	Budget Management
o	save_budget(): Saves or updates the monthly budget.
o	load_budget(): Retrieves the saved budget for the logged-in user.
4.	Transaction Handling
o	add_transaction(): Adds income/expense transactions to the database.
o	display_transactions(): Displays all transactions in a table format.
5.	Report Generation
o	generate_report_page(): Calculates and displays income, expenses, and savings.
6.	UI Navigation
o	switch_frame(): Simplifies switching between different UI frames.

