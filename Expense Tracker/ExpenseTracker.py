import sqlite3
import tkinter as tk
from tkinter import ttk

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL
    )
    """
)
conn.commit()

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if date and category and amount:
        try:
            amount = float(amount)
            cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
            conn.commit()
            status_label.config(text="Expense added successfully!", fg="green")
            date_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
            view_expenses()
        except ValueError:
            status_label.config(text="Invalid amount. Please enter a number.", fg="red")
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        expense_id = expenses_tree.item(selected_item)["values"][0]
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        status_label.config(text="Expense deleted successfully!", fg="green")
        view_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

def view_expenses():
    expenses_tree.delete(*expenses_tree.get_children())
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    total_expense = 0
    for row in rows:
        expenses_tree.insert("", tk.END, values=row)
        total_expense += row[3]  # The amount column
    total_label.config(text=f"Total Expense: {total_expense:.2f}")

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("ID", "Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("ID", text="ID")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.column("ID", width=30)
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create buttons to view and delete expenses
view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=7, column=0, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=7, column=1, padx=5, pady=10)

# Display existing expenses on application start
view_expenses()

root.mainloop()

# Close the database connection when the application exits
conn.close()
