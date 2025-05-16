import tkinter as tk
from tkinter import messagebox, simpledialog
from core.library import DigitalLibrary
from core.book import Book

# Initialize
library = DigitalLibrary()

root = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")

def toggle_ebook_field():
    if ebook_var.get():
        size_entry.config(state='normal')
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state='disabled')

def validate_size(P):
    return P == "" or P.isdigit()

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    size = size_entry.get()
    is_ebook = ebook_var.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "All fields except size are required.")
        return

    try:
        if is_ebook:
            if not size:
                messagebox.showerror("Error", "Download size required for eBooks.")
                return
            library.add_ebook(Book(title, author, isbn), float(size))
        else:
            library.add_book(Book(title, author, isbn))

        update_list()
        messagebox.showinfo("Success", "Book added.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN:")
    try:
        library.lend_book(isbn)
        update_list()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN:")
    try:
        library.return_book(isbn)
        update_list()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN:")
    library.remove_book(isbn)
    update_list()

def search_by_author():
    author = simpledialog.askstring("Author", "Enter author name:")
    results = list(library.books_by_author(author))
    listbox.delete(0, tk.END)
    for book in results:
        listbox.insert(tk.END, str(book))

def update_list():
    listbox.delete(0, tk.END)
    for book in library:
        listbox.insert(tk.END, str(book))

# Widgets
tk.Label(root, text="Title").pack()
title_entry = tk.Entry(root)
title_entry.pack()

tk.Label(root, text="Author").pack()
author_entry = tk.Entry(root)
author_entry.pack()

tk.Label(root, text="ISBN").pack()
isbn_entry = tk.Entry(root)
isbn_entry.pack()

ebook_var = tk.BooleanVar()
tk.Checkbutton(root, text="eBook?", variable=ebook_var, command=toggle_ebook_field).pack()

tk.Label(root, text="Download Size (MB)").pack()
vcmd = (root.register(validate_size), '%P')
size_entry = tk.Entry(root, validate="key", validatecommand=vcmd)
size_entry.pack()
size_entry.config(state='disabled')

tk.Button(root, text="Add Book", command=add_book).pack(pady=5)
tk.Button(root, text="Lend Book", command=lend_book).pack(pady=5)
tk.Button(root, text="Return Book", command=return_book).pack(pady=5)
tk.Button(root, text="Remove Book", command=remove_book).pack(pady=5)
tk.Button(root, text="Search by Author", command=search_by_author).pack(pady=5)

listbox = tk.Listbox(root, width=70)
listbox.pack(pady=10)
update_list()

root.mainloop()
