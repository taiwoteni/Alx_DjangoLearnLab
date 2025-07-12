# Create Operation Documentation

## Command Used
```python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
```

## Expected Output
```
Book created successfully:
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```

## Description
This command creates a new Book instance with the title "1984", author "George Orwell", and publication year 1949. The Django ORM automatically assigns an ID (primary key) to the newly created book object. The `objects.create()` method both creates the object and saves it to the database in a single operation.
