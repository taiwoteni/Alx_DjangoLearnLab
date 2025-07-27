# Update Operation Documentation

## Commands Used
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

## Expected Output
```
Before update:
Title: 1984

Updating title...

After update:
ID: 1
Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

## Description
This operation demonstrates how to update a Book instance:
1. First, retrieve the book using `Book.objects.get(title='1984')`
2. Modify the desired field (in this case, `book.title`)
3. Save the changes to the database using `book.save()`
4. Verify the update by retrieving the book again

The title was successfully changed from "1984" to "Nineteen Eighty-Four" while keeping all other fields unchanged.
