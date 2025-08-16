"""
Comprehensive Unit Tests for API Views

This module contains comprehensive unit tests for all API endpoints including:
- CRUD operations for Book and Author models
- Filtering, searching, and ordering functionality
- Authentication and permission testing
- Error handling and edge cases
- Response data integrity and status code accuracy
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
import json

from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class AuthorAPITestCase(APITestCase):
    """Test cases for Author API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(
            name='John Smith',
            bio='Renowned fiction writer',
            nationality='American'
        )
        
        self.author2 = Author.objects.create(
            name='Jane Doe',
            bio='Expert in programming and technology',
            nationality='British'
        )
        
        # API endpoints
        self.authors_url = '/api/authors/'
        self.author_detail_url = f'/api/authors/{self.author1.id}/'
    
    def test_get_authors_list(self):
        """Test retrieving list of authors."""
        response = self.client.get(self.authors_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check author data
        author_names = [author['name'] for author in response.data['results']]
        self.assertIn('John Smith', author_names)
        self.assertIn('Jane Doe', author_names)
    
    def test_get_author_detail(self):
        """Test retrieving a specific author."""
        response = self.client.get(self.author_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Smith')
        self.assertEqual(response.data['nationality'], 'American')
    
    def test_create_author_authenticated(self):
        """Test creating an author with authentication using force_authenticate."""
        self.client.force_authenticate(user=self.user)
        
        author_data = {
            'name': 'New Author',
            'bio': 'New author biography',
            'nationality': 'Canadian'
        }
        
        response = self.client.post(self.authors_url, author_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Author')
        self.assertTrue(Author.objects.filter(name='New Author').exists())
    
    def test_create_author_authenticated_with_login(self):
        """Test creating an author with authentication using client.login."""
        # Use self.client.login() method for authentication
        login_successful = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_successful)
        
        author_data = {
            'name': 'Login Created Author',
            'bio': 'Author created via login authentication',
            'nationality': 'Canadian'
        }
        
        response = self.client.post(self.authors_url, author_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Login Created Author')
        self.assertTrue(Author.objects.filter(name='Login Created Author').exists())
        
        # Logout after test
        self.client.logout()
    
    def test_create_author_unauthenticated(self):
        """Test creating an author without authentication."""
        author_data = {
            'name': 'New Author',
            'bio': 'New author biography',
            'nationality': 'Canadian'
        }
        
        response = self.client.post(self.authors_url, author_data)
        
        # DRF returns 403 Forbidden for permission denied, not 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_author_authenticated(self):
        """Test updating an author with authentication."""
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'name': 'John Smith Updated',
            'bio': 'Updated biography',
            'nationality': 'American'
        }
        
        response = self.client.put(self.author_detail_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Smith Updated')
        
        # Verify in database
        updated_author = Author.objects.get(id=self.author1.id)
        self.assertEqual(updated_author.name, 'John Smith Updated')
    
    def test_delete_author_authenticated(self):
        """Test deleting an author with authentication."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.author_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author1.id).exists())
    
    def test_author_search(self):
        """Test author search functionality."""
        response = self.client.get(self.authors_url, {'search': 'Smith'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Smith')
    
    def test_author_filtering(self):
        """Test author filtering by nationality."""
        response = self.client.get(self.authors_url, {'nationality': 'American'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nationality'], 'American')


class BookAPITestCase(APITestCase):
    """Test cases for Book API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create test author
        self.author = Author.objects.create(
            name='Test Author',
            bio='Test biography',
            nationality='American'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Python Programming Guide',
            author=self.author,
            isbn='9781234567890',
            publication_year=2023,
            genre='technology',
            pages=350,
            rating=Decimal('4.5'),
            price=Decimal('29.99'),
            description='A comprehensive guide to Python programming.',
            in_stock=True
        )
        
        self.book2 = Book.objects.create(
            title='Fiction Novel',
            author=self.author,
            isbn='9781234567891',
            publication_year=2022,
            genre='fiction',
            pages=280,
            rating=Decimal('4.2'),
            price=Decimal('19.99'),
            description='An exciting fiction novel.',
            in_stock=False
        )
        
        # API endpoints
        self.books_url = '/api/books/'
        self.book_detail_url = f'/api/books/{self.book1.id}/'
    
    def test_get_books_list(self):
        """Test retrieving list of books."""
        response = self.client.get(self.books_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_book_detail(self):
        """Test retrieving a specific book."""
        response = self.client.get(self.book_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python Programming Guide')
        self.assertEqual(response.data['genre'], 'technology')
        self.assertEqual(float(response.data['price']), 29.99)
    
    def test_create_book_authenticated(self):
        """Test creating a book with authentication using force_authenticate."""
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'New Book',
            'author': self.author.id,
            'isbn': '9781234567892',
            'publication_year': 2024,
            'genre': 'mystery',
            'pages': 300,
            'rating': '4.0',
            'price': '25.99',
            'description': 'A new mystery book.',
            'in_stock': True
        }
        
        response = self.client.post(self.books_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertTrue(Book.objects.filter(title='New Book').exists())
    
    def test_create_book_authenticated_with_login(self):
        """Test creating a book with authentication using client.login."""
        # Use self.client.login() method for authentication
        login_successful = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_successful)
        
        book_data = {
            'title': 'Login Created Book',
            'author': self.author.id,
            'isbn': '9781234567893',
            'publication_year': 2024,
            'genre': 'mystery',
            'pages': 300,
            'rating': '4.0',
            'price': '25.99',
            'description': 'A book created via login authentication.',
            'in_stock': True
        }
        
        response = self.client.post(self.books_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Login Created Book')
        self.assertTrue(Book.objects.filter(title='Login Created Book').exists())
        
        # Logout after test
        self.client.logout()
    
    def test_create_book_unauthenticated(self):
        """Test creating a book without authentication."""
        book_data = {
            'title': 'New Book',
            'author': self.author.id,
            'isbn': '9781234567892',
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '25.99'
        }
        
        response = self.client.post(self.books_url, book_data)
        
        # DRF returns 403 Forbidden for permission denied, not 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_authenticated(self):
        """Test updating a book with authentication."""
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'title': 'Updated Python Guide',
            'author': self.author.id,
            'isbn': '9781234567890',
            'publication_year': 2023,
            'genre': 'technology',
            'price': '35.99',
            'description': 'Updated comprehensive guide to Python programming.',
            'in_stock': True
        }
        
        response = self.client.put(self.book_detail_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Python Guide')
        self.assertEqual(float(response.data['price']), 35.99)
    
    def test_partial_update_book(self):
        """Test partial update of a book."""
        self.client.force_authenticate(user=self.user)
        
        update_data = {'price': '39.99'}
        
        response = self.client.patch(self.book_detail_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), 39.99)
        # Title should remain unchanged
        self.assertEqual(response.data['title'], 'Python Programming Guide')
    
    def test_delete_book_authenticated(self):
        """Test deleting a book with authentication."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.book_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_book_search(self):
        """Test book search functionality."""
        response = self.client.get(self.books_url, {'search': 'Python'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Programming Guide')
    
    def test_book_genre_filtering(self):
        """Test book filtering by genre."""
        response = self.client.get(self.books_url, {'genre': 'technology'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['genre'], 'technology')
    
    def test_book_price_range_filtering(self):
        """Test book filtering by price range."""
        response = self.client.get(self.books_url, {
            'price_min': '20.00',
            'price_max': '35.00'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Programming Guide')
    
    def test_book_rating_filtering(self):
        """Test book filtering by minimum rating."""
        response = self.client.get(self.books_url, {'rating_min': '4.3'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Programming Guide')
    
    def test_book_stock_filtering(self):
        """Test book filtering by stock status."""
        response = self.client.get(self.books_url, {'in_stock': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertTrue(response.data['results'][0]['in_stock'])
    
    def test_book_author_name_filtering(self):
        """Test book filtering by author name."""
        response = self.client.get(self.books_url, {'author_name': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_book_ordering_by_price(self):
        """Test book ordering by price."""
        response = self.client.get(self.books_url, {'ordering': 'price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        # First book should be cheaper
        self.assertEqual(float(results[0]['price']), 19.99)
        self.assertEqual(float(results[1]['price']), 29.99)
    
    def test_book_ordering_by_rating_desc(self):
        """Test book ordering by rating (descending)."""
        response = self.client.get(self.books_url, {'ordering': '-rating'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        # First book should have higher rating
        self.assertEqual(float(results[0]['rating']), 4.5)
        self.assertEqual(float(results[1]['rating']), 4.2)
    
    def test_combined_filtering_and_ordering(self):
        """Test combined filtering and ordering."""
        response = self.client.get(self.books_url, {
            'in_stock': 'true',
            'rating_min': '4.0',
            'ordering': '-price'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Python Programming Guide')
    
    def test_pagination(self):
        """Test pagination functionality."""
        response = self.client.get(self.books_url, {'page_size': '1'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn('next', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 2)


class GenericViewsTestCase(APITestCase):
    """Test cases for Generic Views endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(
            name='Generic Test Author',
            bio='Test biography',
            nationality='American'
        )
        
        # Create test book
        self.book = Book.objects.create(
            title='Generic Test Book',
            author=self.author,
            isbn='9781234567899',
            publication_year=2024,
            genre='fiction',
            price=Decimal('24.99'),
            description='Test book for generic views.',
            in_stock=True
        )
        
        # Generic view endpoints
        self.generic_list_url = '/api/books/generic/'
        self.generic_detail_url = f'/api/books/generic/{self.book.id}/'
        self.generic_create_url = '/api/books/generic/create/'
        self.generic_update_url = f'/api/books/generic/{self.book.id}/update/'
        self.generic_delete_url = f'/api/books/generic/{self.book.id}/delete/'
    
    def test_generic_list_view(self):
        """Test generic ListView."""
        response = self.client.get(self.generic_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_generic_detail_view(self):
        """Test generic DetailView."""
        response = self.client.get(self.generic_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Generic Test Book')
    
    def test_generic_create_view_authenticated(self):
        """Test generic CreateView with authentication using force_authenticate."""
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'Generic Created Book',
            'author': self.author.id,
            'isbn': '9781234567898',
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '22.99',
            'description': 'Book created via generic view.',
            'in_stock': True
        }
        
        response = self.client.post(self.generic_create_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Generic Created Book')
    
    def test_generic_create_view_authenticated_with_login(self):
        """Test generic CreateView with authentication using client.login."""
        # Use self.client.login() method for authentication
        login_successful = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_successful)
        
        book_data = {
            'title': 'Login Generic Created Book',
            'author': self.author.id,
            'isbn': '9781234567897',
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '22.99',
            'description': 'Book created via generic view using login.',
            'in_stock': True
        }
        
        response = self.client.post(self.generic_create_url, book_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Login Generic Created Book')
        
        # Logout after test
        self.client.logout()
    
    def test_generic_create_view_unauthenticated(self):
        """Test generic CreateView without authentication."""
        book_data = {
            'title': 'Generic Created Book',
            'author': self.author.id,
            'isbn': '9781234567898',
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '22.99'
        }
        
        response = self.client.post(self.generic_create_url, book_data)
        
        # DRF returns 403 Forbidden for permission denied, not 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_generic_update_view_authenticated(self):
        """Test generic UpdateView with authentication."""
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'title': 'Generic Updated Book',
            'author': self.author.id,
            'isbn': '9781234567899',
            'publication_year': 2024,
            'genre': 'fiction',
            'price': '29.99',
            'description': 'Updated book via generic view.',
            'in_stock': True
        }
        
        response = self.client.put(self.generic_update_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Generic Updated Book')
    
    def test_generic_delete_view_authenticated(self):
        """Test generic DeleteView with authentication."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.generic_delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


class ErrorHandlingTestCase(APITestCase):
    """Test cases for error handling and edge cases."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author = Author.objects.create(
            name='Error Test Author',
            bio='Test biography'
        )
    
    def test_invalid_book_id(self):
        """Test accessing non-existent book."""
        response = self.client.get('/api/books/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_invalid_author_id(self):
        """Test accessing non-existent author."""
        response = self.client.get('/api/authors/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_invalid_data(self):
        """Test creating book with invalid data."""
        self.client.force_authenticate(user=self.user)
        
        invalid_data = {
            'title': '',  # Empty title
            'author': 99999,  # Non-existent author
            'isbn': '123',  # Invalid ISBN (too short)
            'publication_year': 3000,  # Future year
            'price': -10.00  # Negative price
        }
        
        response = self.client.post('/api/books/', invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_duplicate_isbn(self):
        """Test creating book with duplicate ISBN."""
        self.client.force_authenticate(user=self.user)
        
        # Create first book
        Book.objects.create(
            title='First Book',
            author=self.author,
            isbn='9781234567890',
            publication_year=2023,
            genre='fiction',
            price=Decimal('19.99')
        )
        
        # Try to create second book with same ISBN
        duplicate_data = {
            'title': 'Second Book',
            'author': self.author.id,
            'isbn': '9781234567890',  # Duplicate ISBN
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '24.99'
        }
        
        response = self.client.post('/api/books/', duplicate_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('isbn', response.data)
    
    def test_invalid_search_parameters(self):
        """Test search with invalid parameters."""
        response = self.client.get('/api/books/', {
            'price_min': 'invalid',
            'rating_max': 'not_a_number'
        })
        
        # Should still return 200 but with empty results or error handling
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_ordering_field(self):
        """Test ordering by invalid field."""
        response = self.client.get('/api/books/', {'ordering': 'invalid_field'})
        
        # Should return 200 with default ordering
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PermissionTestCase(APITestCase):
    """Test cases for permission and authentication."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.author = Author.objects.create(
            name='Permission Test Author',
            bio='Test biography'
        )
        
        self.book = Book.objects.create(
            title='Permission Test Book',
            author=self.author,
            isbn='9781234567890',
            publication_year=2023,
            genre='fiction',
            price=Decimal('19.99')
        )
    
    def test_read_permissions_unauthenticated(self):
        """Test that unauthenticated users can read data."""
        # Test books list
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test book detail
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test authors list
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test author detail
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_write_permissions_unauthenticated(self):
        """Test that unauthenticated users cannot write data."""
        book_data = {
            'title': 'Unauthorized Book',
            'author': self.author.id,
            'isbn': '9781234567891',
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '24.99'
        }
        
        # Test create - DRF returns 403 Forbidden for permission denied
        response = self.client.post('/api/books/', book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test update
        response = self.client.put(f'/api/books/{self.book.id}/', book_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test delete
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_write_permissions_authenticated(self):
        """Test that authenticated users can write data."""
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'Authorized Book',
            'author': self.author.id,
            'isbn': '9781234567891',
            'publication_year': 2024,
            'genre': 'mystery',
            'price': '24.99',
            'description': 'Test book',
            'in_stock': True
        }
        
        # Test create
        response = self.client.post('/api/books/', book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test update
        book_data['title'] = 'Updated Authorized Book'
        response = self.client.put(f'/api/books/{self.book.id}/', book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test delete
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CustomActionTestCase(APITestCase):
    """Test cases for custom actions in ViewSets."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        self.author = Author.objects.create(
            name='Custom Action Author',
            bio='Test biography'
        )
        
        # Create multiple books for testing
        for i in range(3):
            Book.objects.create(
                title=f'Book {i+1}',
                author=self.author,
                isbn=f'978123456789{i}',
                publication_year=2020 + i,
                genre='fiction',
                rating=Decimal(f'4.{i}'),
                price=Decimal(f'{20 + i}.99')
            )
    
    def test_author_books_action(self):
        """Test custom action to get author's books."""
        response = self.client.get(f'/api/authors/{self.author.id}/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_author_statistics_action(self):
        """Test custom action to get author statistics."""
        response = self.client.get(f'/api/authors/{self.author.id}/statistics/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_books', response.data)
        self.assertIn('average_rating', response.data)
        self.assertEqual(response.data['total_books'], 3)
    
    def test_top_rated_authors_action(self):
        """Test custom action to get top-rated authors."""
        response = self.client.get('/api/authors/top_rated/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_recent_books_action(self):
        """Test custom action to get recent books."""
        response = self.client.get('/api/books/recent/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_books_by_genre_action(self):
        """Test custom action to get books by genre."""
        response = self.client.get('/api/books/by_genre/', {'genre': 'fiction'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_books_in_stock_action(self):
        """Test custom action to get in-stock books."""
        response = self.client.get('/api/books/in_stock/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
