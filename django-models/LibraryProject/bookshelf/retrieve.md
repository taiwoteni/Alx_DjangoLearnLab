# Retrieve Operation Documentation

## Commands Used
```python
from bookshelf.models import Book

# Retrieve all books
all_books = Book.objects.all()
print(f'Total books: {len(all_books)}')
for book in all_books:
    print(f'Book: {book}')

# Retrieve specific book
book = Book.objects.get(title='1984')
print(f'ID: {book.id}')
print(f'Title: {book.title}')
print(f'Author: {book.author}')
print(f'Publication Year: {book.publication_year}')
```

## Expected Output
```
Retrieving all books:
Total books: 1
Book: 1984

Retrieving specific book:
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Description
This operation demonstrates two ways to retrieve book data:
1. `Book.objects.all()` - Retrieves all Book instances from the database
2. `Book.objects.get(title='1984')` - Retrieves a specific Book instance by title

The `__str__` method in our Book model returns the title, which is why "Book: 1984" is displayed when printing the book object.
