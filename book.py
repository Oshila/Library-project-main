import csv
import os

# File path to store all books
DATA_PATH = "data/books.csv"

class Book:
    # This represents a single book in the library

    def __init__(self, book_id, title, author="Unknown", publisher="", publish_date="", available=True, copies=1):
        # Set the book details when a Book object is created
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        # Ensure 'available' is always a boolean (True or False)
        self.available = available == "True" if isinstance(available, str) else available
        self.copies = int(copies)

    def borrow(self):
        # Borrow the book if copies are available
        if self.available:
            self.copies -= 1
            if self.copies == 0:
                self.available = False  # No more copies left
            return True
        return False

    def return_book(self):
        # When a book is returned, increase the number of copies
        self.copies += 1
        self.available = True

    def __str__(self):
        # Display the book details nicely
        return (
            f"Book ID: {self.book_id}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Publisher: {self.publisher}\n"
            f"Publish Date: {self.publish_date}\n"
            f"Copies: {self.copies}\n"
            f"Available: {'Yes' if self.available else 'No'}"
        )

# ----- Helper functions to load, save and find books ----

def load_books():
    # Load all books from the CSV file into a list of Book objects
    books = []
    if not os.path.exists(DATA_PATH):
        return books
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            book = Book(*row)  # Unpack row directly into Book constructor
            books.append(book)
    return books

def save_books(books):
    # Save all Book objects into the CSV file
    with open(DATA_PATH, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for book in books:
            writer.writerow([
                book.book_id,
                book.title,
                book.author,
                book.publisher,
                book.publish_date,
                str(book.available),
                book.copies
            ])

def get_book_by_id(book_id):
    # Find and return a book with the matching ID
    books = load_books()
    for book in books:
        if book.book_id == book_id:
            return book
    return None

