import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from user import Student, create_id, save_student, stud_auth
from librarian import Librarian, create_lib_id, save_librarian, auth_librarian
from library import Library
from book import Book

# -------------------- GUI Class --------------------
class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System – Bells University")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f5f9")
        self.root.resizable(True, True)

        # Library instance
        self.library = Library()
        self.current_user = None
        self.role = None  # "student" or "librarian"

        self.show_welcome_screen()

    # ---------- Utility ----------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- Welcome ----------
    def show_welcome_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Library Management System", font=("Helvetica", 26, "bold"),
                 bg="#f0f5f9", fg="#1a365d").pack(pady=60)

        frame = tk.Frame(self.root, bg="#f0f5f9")
        frame.pack(pady=40)

        tk.Button(frame, text="Student Access", font=("Arial", 16, "bold"), width=40, height=2,
                  bg="#2563eb", fg="white", command=self.show_student_auth).pack(pady=20)

        tk.Button(frame, text="Librarian Access", font=("Arial", 16, "bold"), width=40, height=2,
                  bg="#dc2626", fg="white", command=self.show_librarian_auth).pack(pady=20)

        tk.Button(frame, text="Exit", font=("Arial", 13), width=30, bg="#6b7280", fg="white",
                  command=self.root.quit).pack(pady=30)

    # ---------- STUDENT ----------

    def show_student_auth(self):
        self.clear_screen()
        tk.Label(self.root, text="Student Login / Register", font=("Helvetica", 22),
                 bg="#f0f5f9", fg="#1a365d").pack(pady=50)

        frame = tk.Frame(self.root, bg="#f0f5f9")
        frame.pack()

        tk.Label(frame, text="Student ID:", font=("Arial", 13)).grid(row=0, column=0, pady=15, padx=20, sticky="e")
        self.sid_entry = tk.Entry(frame, width=40, font=("Arial", 13))
        self.sid_entry.grid(row=0, column=1, pady=15)

        tk.Label(frame, text="Password:", font=("Arial", 13)).grid(row=1, column=0, pady=15, padx=20, sticky="e")
        self.spwd_entry = tk.Entry(frame, show="*", width=40, font=("Arial", 13))
        self.spwd_entry.grid(row=1, column=1, pady=15)

        btn_frame = tk.Frame(self.root, bg="#f0f5f9")
        btn_frame.pack(pady=40)

        tk.Button(btn_frame, text="Login", font=("Arial", 13), width=20, bg="#16a34a", fg="white",
                  command=self.student_login).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Register", font=("Arial", 13), width=20, bg="#ea580c", fg="white",
                  command=self.student_register).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Back", font=("Arial", 13), width=20,
                  command=self.show_welcome_screen).pack(side="left", padx=20)

    def student_login(self):
        sid = self.sid_entry.get().strip()
        pwd = self.spwd_entry.get().strip()
        student = stud_auth(sid, pwd)
        if student:
            self.current_user = student
            self.role = "student"
            messagebox.showinfo("Welcome", f"Logged in as {student.name}")
            self.show_student_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def student_register(self):
        name = simpledialog.askstring("Register", "Full Name:")
        if not name: return
        pwd = simpledialog.askstring("Register", "Password:", show="*")
        if not pwd: return
        confirm = simpledialog.askstring("Register", "Confirm Password:", show="*")
        if pwd != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        batch = simpledialog.askstring("Register", "Batch (e.g. 2023):")
        if not batch: return

        sid = create_id()
        student = Student(sid, name, pwd, batch)
        save_student(student)
        messagebox.showinfo("Success", f"Registered!\nYour ID: {sid}\nLogin now.")

    def show_student_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Student Dashboard – {self.current_user.name}",
                 font=("Helvetica", 20, "bold"), bg="#f0f5f9", fg="#1a365d").pack(pady=40)

        buttons = [
            ("View All Books", self.view_books),
            ("Borrow Book", self.borrow_book),
            ("Return Book", self.return_book),
            ("My Borrowed Books", self.view_my_borrowed),
            ("Logout", self.show_welcome_screen)
        ]

        for text, cmd in buttons:
            tk.Button(self.root, text=text, font=("Arial", 14), width=35, height=2,
                      bg="#3b82f6", fg="white", command=cmd).pack(pady=12)

    def view_books(self):
        books = self.library.books
        if not books:
            messagebox.showinfo("Library", "No books available.")
            return
        lines = [f"{b.book_id} | {b.title} – {b.author} | Copies: {b.copies} | {'Available' if b.available else 'Borrowed'}"
                 for b in books]
        messagebox.showinfo("Books", "\n".join(lines))

    def borrow_book(self):
        book_id = simpledialog.askstring("Borrow", "Enter Book ID:")
        if not book_id: return
        book = self.library.get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            return
        if self.current_user.borrow_book(book):
            self.library.save_books()
            messagebox.showinfo("Success", f"You borrowed '{book.title}'.")
        else:
            messagebox.showwarning("Unavailable", "Book not available.")

    def return_book(self):
        book_id = simpledialog.askstring("Return", "Enter Book ID:")
        if not book_id: return
        book = self.library.get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Error", "Book not found.")
            return
        if self.current_user.return_book(book):
            self.library.save_books()
            messagebox.showinfo("Success", f"You returned '{book.title}'.")
        else:
            messagebox.showwarning("Failed", "You didn't borrow this book.")

    def view_my_borrowed(self):
        borrowed = self.current_user.borrowed_books
        if not borrowed:
            messagebox.showinfo("My Books", "No borrowed books.")
            return
        lines = [f"{b.book_id} | {b.title}" for b in borrowed]
        messagebox.showinfo("Borrowed Books", "\n".join(lines))

    # ---------- LIBRARIAN ----------

    def show_librarian_auth(self):
        self.clear_screen()
        tk.Label(self.root, text="Librarian Login / Register", font=("Helvetica", 22),
                 bg="#f0f5f9", fg="#1a365d").pack(pady=50)

        frame = tk.Frame(self.root, bg="#f0f5f9")
        frame.pack()

        tk.Label(frame, text="Librarian ID:", font=("Arial", 13)).grid(row=0, column=0, pady=15, padx=20, sticky="e")
        self.lid_entry = tk.Entry(frame, width=40, font=("Arial", 13))
        self.lid_entry.grid(row=0, column=1, pady=15)

        tk.Label(frame, text="Password:", font=("Arial", 13)).grid(row=1, column=0, pady=15, padx=20, sticky="e")
        self.lpwd_entry = tk.Entry(frame, show="*", width=40, font=("Arial", 13))
        self.lpwd_entry.grid(row=1, column=1, pady=15)

        btn_frame = tk.Frame(self.root, bg="#f0f5f9")
        btn_frame.pack(pady=40)

        tk.Button(btn_frame, text="Login", font=("Arial", 13), width=20, bg="#16a34a", fg="white",
                  command=self.librarian_login).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Register", font=("Arial", 13), width=20, bg="#ea580c", fg="white",
                  command=self.librarian_register).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Back", font=("Arial", 13), width=20,
                  command=self.show_welcome_screen).pack(side="left", padx=20)

    def librarian_login(self):
        lid = self.lid_entry.get().strip()
        pwd = self.lpwd_entry.get().strip()
        librarian = auth_librarian(lid, pwd)
        if librarian:
            self.current_user = librarian
            self.role = "librarian"
            messagebox.showinfo("Welcome", f"Logged in as {librarian.name}")
            self.show_librarian_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def librarian_register(self):
        name = simpledialog.askstring("Register", "Full Name:")
        if not name: return
        pwd = simpledialog.askstring("Register", "Password:", show="*")
        if not pwd: return
        confirm = simpledialog.askstring("Register", "Confirm Password:", show="*")
        if pwd != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        lid = create_lib_id()
        librarian = Librarian(lid, name, pwd)
        save_librarian(librarian)
        messagebox.showinfo("Success", f"Registered!\nYour ID: {lid}\nLogin now.")

    def show_librarian_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Librarian Dashboard – {self.current_user.name}",
                 font=("Helvetica", 20, "bold"), bg="#f0f5f9", fg="#1a365d").pack(pady=40)

        buttons = [
            ("View All Books", self.view_books),
            ("Add Book", self.add_book),
            ("Remove Book", self.remove_book),
            ("Logout", self.show_welcome_screen)
        ]

        for text, cmd in buttons:
            tk.Button(self.root, text=text, font=("Arial", 14), width=35, height=2,
                      bg="#ef4444", fg="white", command=cmd).pack(pady=12)

    def add_book(self):
        book_id = simpledialog.askstring("Add Book", "Book ID:")
        if not book_id: return
        title = simpledialog.askstring("Add Book", "Title:")
        author = simpledialog.askstring("Add Book", "Author:")
        publisher = simpledialog.askstring("Add Book", "Publisher:")
        pub_date = simpledialog.askstring("Add Book", "Publish Date (YYYY-MM-DD):")
        copies = simpledialog.askinteger("Add Book", "Number of Copies:")
        if not all([book_id, title, copies]):
            messagebox.showerror("Error", "Book ID, Title, and Copies are required.")
            return
        book = Book(book_id, title, author, publisher, pub_date, True, copies)
        self.current_user.add_book(self.library, book)
        self.library.save_books()
        messagebox.showinfo("Success", f"Book '{title}' added.")

    def remove_book(self):
        book_id = simpledialog.askstring("Remove Book", "Enter Book ID:")
        if not book_id: return
        self.current_user.remove_book(self.library, book_id)
        self.library.save_books()
        messagebox.showinfo("Success", f"Book {book_id} removed.")

# -------------------- Start GUI --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
