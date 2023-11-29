#README: This is still work in progress, I added some comments to the code to explain what it does.

#Import packages
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


#Search Books function to find books
def search_books():
    query = search_entry.get().lower()
    
    # Clear previous search results
    for item in tree.get_children():
        tree.delete(item)

    # Iterate through your data and find matches
    for book in library_data:
        if query in book["ISBN"].lower() or query in book["Book Title"].lower() or query in book["Author"].lower():
            tree.insert("", "end", text=book["ISBN"], values=(book["Book Title"], book["Author"], book["Genre"], book["Year"]))
            
#Checkout books function to select books for checkout.
def checkout_books():
    selected_items = tree.selection()
    
#If books haven't been selected for checkout, return error.
    if not selected_items:
        tk.messagebox.showinfo("Checkout", "Please select at least one book for checkout.")
        return

    # Prompt for borrower's card number
    card_number = tk.simpledialog.askstring("Checkout", "Enter Borrower's Card Number:")
    if not card_number:
        return  # User canceled the input

    # Generate unique keys for each checkout
    checkout_ids = [str(datetime.now().timestamp()) for _ in selected_items]

    # Get today's date for date_out
    date_out = datetime.today().strftime("%Y-%m-%d")

    # Calculate due_date (14 days after date_out)
    due_date = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Update the BOOK_LOANS table (replace this with your actual database update logic)
    for item, checkout_id in zip(selected_items, checkout_ids):
        book_title = tree.item(item, "values")[0]  # Assuming the book title is in the first column
        # Insert the checkout information into the BOOK_LOANS table (replace this with your actual database update logic)
        print(f"Book '{book_title}' checked out with Checkout ID: {checkout_id}, Card Number: {card_number}, Date Out: {date_out}, Due Date: {due_date}")

#Successful checkout
    tk.messagebox.showinfo("Checkout", "Books checked out successfully.")
    
    


# Create a main window
root = tk.Tk()
root.title("Library Database")

# Add a search field and button
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

search_label = ttk.Label(search_frame, text="Search:")
search_label.grid(row=0, column=0)

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=0, column=1)

search_button = ttk.Button(search_frame, text="Search", command=search_books)
search_button.grid(row=0, column=2)

# Your library data (replace this with your actual data)
library_data = [
    {"ISBN": "1", "Book Title": "Harry Potter", "Author": "J.K. Rowling", "Genre": "Fantasy", "Year": "1997"},
    {"ISBN": "2", "Book Title": "To Kill a Mockingbird", "Author": "Harper Lee", "Genre": "Fiction", "Year": "1960"},
    {"ISBN": "3", "Book Title": "The Lord of the Rings", "Author": "J. R. R. Tolkien", "Genre": "Non-Fiction", "Year": "1955"},
    {"ISBN": "4", "Book Title": "1984"}
    
]


# Create a treeview to display the data
tree = ttk.Treeview(root)
tree["columns"] = ("Book Title", "Author", "Genre", "Year")

# Define columns
tree.column("#0", width=0, stretch=tk.NO)
tree.column("Book Title", anchor=tk.W, width=150)
tree.column("Author", anchor=tk.W, width=100)
tree.column("Genre", anchor=tk.W, width=100)
tree.column("Year", anchor=tk.W, width=70)

# Add headings
tree.heading("#0", text="", anchor=tk.W)
tree.heading("Book Title", text="Book Title", anchor=tk.W)
tree.heading("Author", text="Author", anchor=tk.W)
tree.heading("Genre", text="Genre", anchor=tk.W)
tree.heading("Year", text="Year", anchor=tk.W)

# Inserting sample data into the treeview
tree.insert("", "end", text="1", values=("Harry Potter", "J.K. Rowling", "Fantasy", "1997"))
tree.insert("", "end", text="2", values=("To Kill a Mockingbird", "Harper Lee", "Fiction", "1960"))
tree.insert("", "end", text="3", values=("1984", "George Orwell", "Dystopian", "1949"))
tree.insert("", "end", text="4", values=("Why AI is the future and gonna change the world", "Yash Hooda", "Non-Fiction", "2023"))
tree.insert("", "end", text="5", values=("The Lord of the Rings", "J. R. R. Tolkien", "Non-Fiction", "1955"))

# Place the treeview
tree.pack(padx=10, pady=10)


# Add a button for checking out books
checkout_button = ttk.Button(root, text="Checkout Selected Books", command=checkout_books)
checkout_button.pack(pady=10)

# Run the main loop
root.mainloop()