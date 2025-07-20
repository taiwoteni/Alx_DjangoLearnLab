from .models import Author, Book, Library, Librarian

# Get an author by name
def get_author(author_name):
    return Author.objects.get(name=author_name)

# Query all books by a specific author name
def get_books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)

# Query all books by an Author object
def get_books_by_author_object(author):
    return Book.objects.filter(author=author)

# List all books in a library
def get_books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()

# Retrieve the librarian for a library by name
def get_librarian_for_library(library_name):
    return Librarian.objects.get(library__name=library_name)

# Retrieve the librarian for a Library object
def get_librarian_for_library_object(library):
    return Librarian.objects.get(library=library)
