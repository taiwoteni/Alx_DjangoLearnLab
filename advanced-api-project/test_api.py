#!/usr/bin/env python3
"""
Comprehensive API Testing Script

This script provides a complete testing suite for the advanced API project,
including model creation, serialization testing, and API endpoint validation.
"""

import os
import sys
import django

# Add the project to the Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date
from decimal import Decimal
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer


class ModelTests(TestCase):
    """Test cases for the Author and Book models."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(
            name="Test Author",
            bio="A test author biography",
            nationality="Testland",
            birth_date=date(1980, 1, 1)
        )
        
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            publication_year=2023,
            genre="fiction",
            pages=300,
            rating=4.5,
            price=Decimal("29.99"),
            in_stock=True,
            description="A test book description"
        )
    
    def test_author_creation(self):
        """Test author model creation."""
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(self.author.bio, "A test author biography")
        self.assertEqual(str(self.author), "Test Author")
    
    def test_book_creation(self):
        """Test book model creation."""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(str(self.book), "Test Book by Test Author")
    
    def test_book_year_validation(self):
        """Test book publication year validation."""
        # Test future year validation
        with self.assertRaises(ValueError):
            Book.objects.create(
                title="Future Book",
                author=self.author,
                publication_year=2030,  # Future year
                genre="fiction",
                pages=200,
                rating=4.0,
                price=Decimal("19.99")
            )
    
    def test_author_book_relationship(self):
        """Test the relationship between Author and Book."""
        self.assertEqual(self.author.books.count(), 1)
        self.assertEqual(self.author.books.first(), self.book)


class SerializerTests(TestCase):
    """Test cases for the Author and Book serializers."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(
            name="Test Author",
            bio="A test author biography",
            nationality="Testland",
            birth_date=date(1980, 1, 1)
        )
        
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author=self.author,
            isbn="1234567890123",
            publication_year=2023,
            genre="fiction",
            pages=300,
            rating=4.5,
            price=Decimal("29.99"),
            in_stock=True
        )
        
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author=self.author,
            isbn="9876543210987",
            publication_year=2022,
            genre="mystery",
            pages=250,
            rating=4.2,
            price=Decimal("24.99"),
            in_stock=False
        )
    
    def test_author_serializer(self):
        """Test AuthorSerializer with nested books."""
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        
        self.assertEqual(data['name'], "Test Author")
        self.assertEqual(len(data['books']), 2)
        self.assertEqual(data['books'][0]['title'], "Test Book 1")
    
    def test_book_serializer(self):
        """Test BookSerializer."""
        serializer = BookSerializer(self.book1)
        data = serializer.data
        
        self.assertEqual(data['title'], "Test Book 1")
        self.assertEqual(data['author']['name'], "Test Author")
        self.assertEqual(data['publication_year'], 2023)
    
    def test_book_serializer_validation(self):
        """Test BookSerializer validation."""
        # Test valid data
        valid_data = {
            'title': 'New Book',
            'author': self.author.id,
            'publication_year': 2023,
            'genre': 'FICTION',
            'pages': 200,
            'rating': 4.0,
            'price': 19.99
        }
        
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Test invalid future year
        invalid_data = valid_data.copy()
        invalid_data['publication_year'] = 2030
        
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)


class APITests(APITestCase):
    """Test cases for API endpoints."""
    
    def setUp(self):
        """Set up test data and client."""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
        self.author1 = Author.objects.create(
            name="Author One",
            bio="First test author",
            nationality="Country1",
            birth_date=date(1975, 5, 15)
        )
        
        self.author2 = Author.objects.create(
            name="Author Two",
            bio="Second test author",
            nationality="Country2",
            birth_date=date(1985, 8, 20)
        )
        
        self.book1 = Book.objects.create(
            title="Book One",
            author=self.author1,
            isbn="1111111111111",
            publication_year=2023,
            genre="fiction",
            pages=300,
            rating=4.5,
            price=Decimal("29.99"),
            in_stock=True
        )
        
        self.book2 = Book.objects.create(
            title="Book Two",
            author=self.author1,
            isbn="2222222222222",
            publication_year=2022,
            genre="mystery",
            pages=250,
            rating=4.2,
            price=Decimal("24.99"),
            in_stock=False
        )
        
        self.book3 = Book.objects.create(
            title="Book Three",
            author=self.author2,
            isbn="3333333333333",
            publication_year=2021,
            genre="sci-fi",
            pages=400,
            rating=4.8,
            price=Decimal("39.99"),
            in_stock=True
        )
    
    def test_author_list(self):
        """Test GET /api/authors/ endpoint."""
        url = reverse('author-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_author_detail(self):
        """Test GET /api/authors/{id}/ endpoint."""
        url = reverse('author-detail', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Author One")
        self.assertEqual(len(response.data['books']), 2)
    
    def test_book_list(self):
        """Test GET /api/books/ endpoint."""
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_book_detail(self):
        """Test GET /api/books/{id}/ endpoint."""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Book One")
        self.assertEqual(response.data['author']['name'], "Author One")
    
    def test_create_author(self):
        """Test POST /api/authors/ endpoint."""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('author-list')
        data = {
            'name': 'New Author',
            'bio': 'A new test author',
            'nationality': 'New Country',
            'birth_date': '1990-01-01'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 3)
    
    def test_create_book(self):
        """Test POST /api/books/ endpoint."""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': self.author1.id,
            'isbn': '4444444444444',
            'publication_year': 2023,
            'genre': 'FICTION',
            'pages': 350,
            'rating': 4.3,
            'price': 34.99,
            'in_stock': True
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
    
    def test_author_books_endpoint(self):
        """Test GET /api/authors/{id}/books/ endpoint."""
        url = reverse('author-books', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_author_statistics_endpoint(self):
        """Test GET /api/authors/{id}/statistics/ endpoint."""
        url = reverse('author-statistics', kwargs={'pk': self.author1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_books'], 2)
        self.assertIsNotNone(response.data['average_rating'])
    
    def test_book_search_endpoint(self):
        """Test GET /api/books/search/ endpoint."""
        url = reverse('book-search')
        response = self.client.get(url, {'q': 'Book'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 3)
    
    def test_book_filtering(self):
        """Test book filtering by genre."""
        url = reverse('book-list')
        response = self.client.get(url, {'genre': 'FICTION'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Book One")
    
    def test_book_price_filtering(self):
        """Test book filtering by price range."""
        url = reverse('book-list')
        response = self.client.get(url, {
            'price_min': 25,
            'price_max': 35
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_author_top_rated_endpoint(self):
        """Test GET /api/authors/top-rated/ endpoint."""
        url = reverse('author-top-rated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
    
    def test_book_recent_endpoint(self):
        """Test GET /api/books/recent/ endpoint."""
        url = reverse('book-recent')
        response = self.client.get(url, {'years': 3})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)


def run_tests():
    """Run all tests."""
    print("Running Django Advanced API Tests...")
    print("=" * 50)
    
    # Run model tests
    print("\n1. Testing Models...")
    model_tests = ModelTests()
    model_tests.setUp()
    model_tests.test_author_creation()
    model_tests.test_book_creation()
    model_tests.test_book_year_validation()
    model_tests.test_author_book_relationship()
    print("✓ Model tests passed")
    
    # Run serializer tests
    print("\n2. Testing Serializers...")
    serializer_tests = SerializerTests()
    serializer_tests.setUp()
    serializer_tests.test_author_serializer()
    serializer_tests.test_book_serializer()
    serializer_tests.test_book_serializer_validation()
    print("✓ Serializer tests passed")
    
    # Run API tests
    print("\n3. Testing API Endpoints...")
    api_tests = APITests()
    api_tests.setUp()
    
    # Test basic endpoints
    api_tests.test_author_list()
    api_tests.test_author_detail()
    api_tests.test_book_list()
    api_tests.test_book_detail()
    print("✓ Basic API tests passed")
    
    # Test custom endpoints
    api_tests.test_author_books_endpoint()
    api_tests.test_author_statistics_endpoint()
    api_tests.test_book_search_endpoint()
    api_tests.test_book_filtering()
    api_tests.test_book_price_filtering()
    api_tests.test_author_top_rated_endpoint()
    api_tests.test_book_recent_endpoint()
    print("✓ Custom API tests passed")
    
    print("\n" + "=" * 50)
    print("All tests completed successfully! 🎉")
    print("\nTo run the development server:")
    print("python3 manage.py runserver")
    print("\nTo access the API:")
    print("http://localhost:8000/api/")
    print("http://localhost:8000/admin/")
    print("http://localhost:8000/api-auth/login/")


if __name__ == '__main__':
    run_tests()
