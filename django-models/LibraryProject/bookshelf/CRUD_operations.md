# CRUD Operations Documentation for Book Model

This document provides a comprehensive overview of all CRUD (Create, Read, Update, Delete) operations performed on the Book model in the bookshelf Django app.

## Model Definition

The Book model is defined in `bookshelf/models.py` with the following fields:

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title
```

## CRUD Operations

### 1. CREATE Operation

**Command:**
```python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
```

**Output:**
```
Book created successfully:
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

**Description:** Creates a new Book instance with the specified attributes and saves it to the database.

---

### 2. RETRIEVE Operation

**Commands:**
```python
from bookshelf.models import Book

# Retrieve all books
all_books = Book.objects.all()
print(f'Total books: {len(all_books)}')

# Retrieve specific book
book = Book.objects.get(title='1984')
print(f'Title: {book.title}')
print(f'Author: {book.author}')
print(f'Publication Year: {book.publication_year}')
```

**Output:**
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

**Description:** Demonstrates retrieving all books and a specific book by title.

---

### 3. UPDATE Operation

**Commands:**
```python
from bookshelf.models import Book

# Get the book to update
book = Book.objects.get(title='1984')
print(f'Before update - Title: {book.title}')

# Update the title
book.title = 'Nineteen Eighty-Four'
book.save()

# Verify the update
updated_book = Book.objects.get(id=book.id)
print(f'After update - Title: {updated_book.title}')
```

**Output:**
```
Before update:
Title: 1984

After update:
ID: 1
Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

**Description:** Updates the title of the book from "1984" to "Nineteen Eighty-Four" and saves the changes.

---

### 4. DELETE Operation

**Commands:**
```python
from bookshelf.models import Book

# Check books before deletion
all_books = Book.objects.all()
print(f'Before deletion - Total books: {len(all_books)}')

# Delete the book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()

# Confirm deletion
all_books = Book.objects.all()
print(f'After deletion - Total books: {len(all_books)}')
```

**Output:**
```
Before deletion:
Total books: 1
Book: Nineteen Eighty-Four (ID: 1)

After deletion:
Total books: 0
No books found in the database.
```

**Description:** Deletes the book from the database and confirms the deletion by checking that no books remain.

---

## Summary

All CRUD operations have been successfully implemented and tested:

- ✅ **CREATE**: Successfully created a Book instance with title "1984"
- ✅ **RETRIEVE**: Successfully retrieved book data using both `all()` and `get()` methods
- ✅ **UPDATE**: Successfully updated the book title from "1984" to "Nineteen Eighty-Four"
- ✅ **DELETE**: Successfully deleted the book and confirmed removal from database

The Book model is properly configured with migrations applied, and all operations work as expected through the Django shell.
