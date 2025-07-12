# Delete Operation Documentation

## Commands Used
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

## Expected Output
```
Before deletion:
Total books: 1
Book: Nineteen Eighty-Four (ID: 1)

Deleting the book...

After deletion:
Total books: 0
No books found in the database.
```

## Description
This operation demonstrates how to delete a Book instance:
1. First, check the current state by retrieving all books with `Book.objects.all()`
2. Get the specific book to delete using `Book.objects.get(title='Nineteen Eighty-Four')`
3. Delete the book using the `delete()` method
4. Confirm the deletion by checking that no books remain in the database

The book was successfully removed from the database, as confirmed by the total count changing from 1 to 0.
