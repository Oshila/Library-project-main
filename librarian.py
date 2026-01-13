import csv
import os

# File path where librarian data is stored
DATA_PATH = "data/librarian.csv"

class Librarian:
    """ this represents a librarian who can manage books."""

    def __init__(self, librarian_id, name, password=None):
        self.librarian_id = librarian_id  #ID that belongs to the librarian
        self.name = name                  # Name of the librarian
        self.password = password          # Password used for login (kept private)

    def add_book(self, library, book):
        # this adds a new book to the library
        library.add_book(book)
        print(f"Librarian {self.name} added '{book.title}'.")

    def remove_book(self, library, book_id):
        #removes a book from the library using its ID
        if library.remove_book(book_id):
            print(f"Librarian {self.name} removed book with ID {book_id}.")
        else:
            print(f"Book with ID {book_id} not found.")

    def __str__(self):
        #returns the librarian details as a simple sentence
        return f"Librarian ID: {self.librarian_id}, Name: {self.name}"


# -----Helper functions used for librarian login and saving----

def create_lib_id():
    #creates a new ID for a librarian like lb0001, lb0002
    if not os.path.exists(DATA_PATH):
        return "lb0001"

    with open(DATA_PATH, newline='') as f:
        rows = list(csv.reader(f))
        if not rows:
            return "lb0001"

        last_id = rows[-1][0]          #Get the last librarian ID
        num = int(last_id[2:]) + 1     #Increase the number
        return f"lb{num:04d}"          #Format it with 4 digits (like lb0005)

def save_librarian(lib):
    # This function saves the librarian details into the file
    with open(DATA_PATH, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([lib.librarian_id, lib.name, lib.password])
    print(f"Librarian {lib.name} saved successfully.")

def auth_librarian(lib_id, password):
    # checks if a librarian ID and password match what's saved in the file
    if not os.path.exists(DATA_PATH):
        return None

    with open(DATA_PATH, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == lib_id and row[2] == password:
                return Librarian(row[0], row[1], row[2])  # Return librarian info if it is found

    return None  # Return nothing if no match
