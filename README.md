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
   
    -	Secure registration and login functionality.
      
    -	Passwords are stored as plain text (for simplicity; for real-world applications, hashing is recommended).
      
2.	Budget Management
   
    -	Users can set and update a monthly budget.
      
    -	Budgets are user-specific and tracked independently.
      
3.	Transaction Management
   
    -	Add transactions categorized as income or expenses.
      
    -	Include details like date, category, amount, and description.
      
    -	Warn users if expenses exceed the monthly budget.
      
4.	Report Generation
   
    -	Summarize total income, expenses, and net savings.
      
    -	Display financial reports directly in the application.
      
________________________________________

Installation Instructions

1.	Prerequisites
   
    -	Python 3.x installed on your system.
      
    -	Required Python libraries: tkinter, sqlite3, datetime.
      
2.	Setup
   
    -	Save the script as finance_manager.py in a folder.
      
    -	Run the script to initialize the database:  finance_manager.py
      
________________________________________

Usage Guide

Starting the Application

  1.	Run the script:   "finance_manager.py"
   
  2.	Home Screen
   
      -	Click on Login if you already have an account.
      
      -	Click on Register to create a new account.
      
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
     
    -	Date: Use the format YYYY-MM-DD.
    
    -	Category: Select from predefined options like Food, Transport, etc.
    
    -	Type: Choose between Income or Expense.
    
    -	Amount: Enter a numeric value.
    
    -	Description: Optionally, add details about the transaction.
    
  2.	Click Add Transaction to save the transaction.
     
  3.	If the transaction exceeds your monthly budget, a warning message is displayed.
Viewing Transactions

  4.	All transactions are displayed in a table format, showing:
  
    -	Date, Category, Type, Amount, and Description.
    
  5.  Generating Reports

    1.	Click on Generate Report to view a summary of:
     
      -	Total income.
    
      -	Total expenses.
    
      -	Net savings.
    
  6.  Returning to the Main Menu

    -	Click Back to navigate between pages.
    
________________________________________

Code Structure

1.	Database Setup

    -	The setup_database() function creates three tables:
      
        -	users: Stores user credentials.
          
        -	transactions: Logs all transactions for users.
          
        -	budgets: Saves user-specific monthly budgets.
          
2.	Authentication Functions
   
    -	register_user(): Handles user registration.
      
    -	login_user(): Verifies login credentials and loads user data.
      
3.	Budget Management
   
    -	save_budget(): Saves or updates the monthly budget.
      
    -	load_budget(): Retrieves the saved budget for the logged-in user.
      
4.	Transaction Handling
   
    -	add_transaction(): Adds income/expense transactions to the database.
      
    -	display_transactions(): Displays all transactions in a table format.
      
5.	Report Generation
   
    -	generate_report_page(): Calculates and displays income, expenses, and savings.
      
6.	UI Navigation
   
    -	switch_frame(): Simplifies switching between different UI frames.
      

