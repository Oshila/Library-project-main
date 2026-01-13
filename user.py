import csv
from book import Book  # Import Book class so students can borrow and return books


class Student:
    # Represents a student in the library system

    def __init__(self, student_id, name, password, batch):
        self.student_id = student_id        # Unique ID assigned to the student
        self.name = name                    # Student's name
        self.password = password            # Student's password (stored in plain text)
        self.batch = batch                  # Student's batch or department
        self.borrowed_books = []            # List of borrowed books

    def borrow_book(self, book):
        # Tries to borrow a book and adds it to borrowed list if successful
        if book.borrow():
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed '{book.title}'.")
        else:
            print(f"'{book.title}' not available.")

    def return_book(self, book):
        # Returns a book if it was borrowed
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            print(f"{self.name} returned '{book.title}'.")
        else:
            print("You didn't borrow this book.")

    def deregister(self):
        # Logs the student as deregistered (does not remove from file)
        print(f"{self.name} deregistered.")
        return True

    def list_borrowed_books(self):
        # Lists all books the student has borrowed
        if not self.borrowed_books:
            print("No books borrowed.")
        else:
            for b in self.borrowed_books:
                print(f"- {b.title} (ID: {b.book_id})")


# ===== Helper Functions =====

def create_id():
    # Creates a new student ID by reading the last ID from students.csv
    try:
        with open("data/students.csv", "r") as f:
            lines = list(csv.reader(f))
            last = lines[-1][0]           # Get last student ID like'st0002'
            num = int(last[2:]) + 1       # Extract number and increment
            return f"st{num:04d}"         # Format new ID like'st0003'
    except:
        return "st0001"                  # Start from st0001 if file doesn't exist or is empty


def save_student(student):
    # Saves a new student's information to students.csv
    with open("data/students.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([student.student_id, student.name, student.password, student.batch])
    print("Student saved.")


def stud_auth(sid, pwd):
    # Authenticates a student using ID and password
    try:
        with open("data/students.csv", "r") as f:
            for row in csv.reader(f):
                if row[0] == sid and row[2] == pwd:
                    return Student(row[0], row[1], row[2], row[3])
    except FileNotFoundError:
        print("students.csv not found.")
    return None
