#!/usr/bin/env python3
"""
Simple Generic Views Test Script

This script tests the generic views using Django's test client
without requiring a running server.
"""

import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from api.models import Author, Book
import json

class GenericViewsTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test author
        self.author = Author.objects.create(
            name="Test Author",
            bio="Test biography",
            nationality="Testland"
        )
        
        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            publication_year=2024,
            genre="fiction",
            price=19.99,
            rating=4.5,
            description="Test book description",
            in_stock=True
        )

    def test_book_list_view(self):
        """Test BookListView."""
        response = self.client.get('/api/books/generic/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('results', data)
        print("✅ BookListView test passed")

    def test_book_detail_view(self):
        """Test BookDetailView."""
        response = self.client.get(f'/api/books/generic/{self.book.id}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Test Book")
        print("✅ BookDetailView test passed")

    def test_book_create_view_unauthenticated(self):
        """Test BookCreateView without authentication."""
        new_book_data = {
            "title": "New Test Book",
            "author": self.author.id,
            "isbn": "9876543210987",
            "publication_year": 2024,
            "genre": "fiction",
            "price": 24.99
        }
        response = self.client.post(
            '/api/books/generic/create/',
            data=json.dumps(new_book_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)  # Unauthorized
        print("✅ BookCreateView unauthenticated test passed")

    def test_book_create_view_authenticated(self):
        """Test BookCreateView with authentication."""
        self.client.login(username='testuser', password='testpass123')
        new_book_data = {
            "title": "New Test Book",
            "author": self.author.id,
            "isbn": "9876543210987",
            "publication_year": 2024,
            "genre": "fiction",
            "price": 24.99
        }
        response = self.client.post(
            '/api/books/generic/create/',
            data=json.dumps(new_book_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)  # Created
        data = json.loads(response.content)
        self.assertEqual(data['title'], "New Test Book")
        print("✅ BookCreateView authenticated test passed")

    def test_book_update_view(self):
        """Test BookUpdateView."""
        self.client.login(username='testuser', password='testpass123')
        update_data = {"price": 29.99}
        response = self.client.put(
            f'/api/books/generic/{self.book.id}/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(float(data['price']), 29.99)
        print("✅ BookUpdateView test passed")

    def test_book_delete_view(self):
        """Test BookDeleteView."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(
            f'/api/books/generic/{self.book.id}/delete/'
        )
        self.assertEqual(response.status_code, 204)  # No Content
        print("✅ BookDeleteView test passed")

    def test_book_search_view(self):
        """Test BookSearchView."""
        response = self.client.get('/api/books/generic/search/?q=test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('results', data)
        print("✅ BookSearchView test passed")

    def test_book_by_genre_view(self):
        """Test BookByGenreListView."""
        response = self.client.get('/api/books/generic/genre/fiction/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('results', data)
        print("✅ BookByGenreListView test passed")

def run_tests():
    """Run all tests."""
    print("🧪 Running Generic Views Tests...")
    print("=" * 50)
    
    test = GenericViewsTest()
    test.setUp()
    
    try:
        test.test_book_list_view()
        test.test_book_detail_view()
        test.test_book_create_view_unauthenticated()
        test.test_book_create_view_authenticated()
        test.test_book_update_view()
        test.test_book_delete_view()
        test.test_book_search_view()
        test.test_book_by_genre_view()
        
        print("=" * 50)
        print("🎉 All generic views tests passed!")
        print("✅ Generic views are working correctly")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    run_tests()
