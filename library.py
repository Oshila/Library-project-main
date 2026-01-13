import csv
from book import Book

# Path to the books CSV file
BOOKS_FILE = 'data/books.csv'

class Library:
    #Handles all book-related operations in the library.
    def __init__(self):
        # Load books from file when library is initialized
        self.books = self.load_books()

    def load_books(self):

        #Loads books from the CSV file into memory as Book objects,and if file is not found, it start with an empty list.
        books = []
        try:
            with open(BOOKS_FILE, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 7:

                        continue

                        continue #skip row with missng data
    
                    book_id = row[0]
                    title = row[1]
                    author = row[2]
                    publisher = row[3]
                    publish_date = row[4]
                    available = row[5] == "True"
                    copies = int(row[6])

                    # Create a Book object with all correct values
                    book = Book(book_id, title, author, publisher, publish_date, True, copies)
                    book.available = available
                    books.append(book)
        except FileNotFoundError:
            print(f"{BOOKS_FILE} not found. Starting with empty library.")
        return books

#Saves the list of books to the CSV file.

    def save_books(self):
        with open(BOOKS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for book in self.books:
                writer.writerow([
                    book.book_id,
                    book.title,
                    book.author,
                    book.publisher,
                    book.publish_date,
                    book.available,
                    book.copies
                ])

#Adds a new book and saves the updated book list to file.

    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        print(f"Book '{book.title}' added successfully.")


#Removes a book from the list using its ID.
    def remove_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

#show all books currently in the library.
    def list_all_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            print("Books in the Library:")
            for book in self.books:
                print(book)
                print('-' * 40)

# search for a book and returns a book by its ID.
    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None
