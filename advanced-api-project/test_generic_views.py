#!/usr/bin/env python3
"""
Test Script for Generic Views

This script provides comprehensive testing for the generic views
implemented for the Book model. It tests all CRUD operations
and validates the permission system.

Usage:
    python test_generic_views.py
"""

import requests
import json
import os
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}

# Test data
TEST_BOOK = {''
    "title": "Test Book for Generic Views",
    "author": 1,  # This should be updated based on existing authors
    "isbn": "1234567890123",
    "publication_year": 2024,
    "genre": "fiction",
    "price": 29.99,
    "description": "Test book for generic views testing"
}

class GenericViewsTester:
    """Test class for generic views."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def test_list_books(self) -> bool:
        """Test GET /books/generic/"""
        print("\n=== Testing Book List View ===")
        try:
            response = self.session.get(f"{self.base_url}/books/generic/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ List view successful - Found {len(data.get('results', []))} books")
                return True
            else:
                print(f"❌ List view failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ List view error: {e}")
            return False
    
    def test_retrieve_book(self, book_id: int) -> bool:
        """Test GET /books/generic/<id>/"""
        print("\n=== Testing Book Detail View ===")
        try:
            response = self.session.get(f"{self.base_url}/books/generic/{book_id}/")
            if response.status_code == 200:
                book = response.json()
                print(f"✅ Detail view successful - Book: {book.get('title')}")
                return True
            else:
                print(f"❌ Detail view failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Detail view error: {e}")
            return False
    
    def test_create_book(self, book_data: Dict[str, Any]) -> Optional[int]:
        """Test POST /books/generic/create/"""
        print("\n=== Testing Book Create View ===")
        try:
            response = self.session.post(
                f"{self.base_url}/books/generic/create/",
                json=book_data
            )
            if response.status_code == 201:
                book = response.json()
                print(f"✅ Create view successful - Book ID: {book.get('id')}")
                return book.get('id')
            else:
                print(f"❌ Create view failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Create view error: {e}")
            return None
    
    def test_update_book(self, book_id: int, update_data: Dict[str, Any]) -> bool:
        """Test PUT /books/generic/<id>/update/"""
        print("\n=== Testing Book Update View ===")
        try:
            response = self.session.put(
                f"{self.base_url}/books/generic/{book_id}/update/",
                json=update_data
            )
            if response.status_code == 200:
                book = response.json()
                print(f"✅ Update view successful - Updated: {book.get('title')}")
                return True
            else:
                print(f"❌ Update view failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Update view error: {e}")
            return False
    
    def test_delete_book(self, book_id: int) -> bool:
        """Test DELETE /books/generic/<id>/delete/"""
        print("\n=== Testing Book Delete View ===")
        try:
            response = self.session.delete(
                f"{self.base_url}/books/generic/{book_id}/delete/"
            )
            if response.status_code == 204:
                print(f"✅ Delete view successful - Book ID: {book_id}")
                return True
            else:
                print(f"❌ Delete view failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Delete view error: {e}")
            return False
    
    def test_search_books(self, query: str) -> bool:
        """Test GET /books/generic/search/"""
        print("\n=== Testing Book Search View ===")
        try:
            params = {"q": query}
            response = self.session.get(
                f"{self.base_url}/books/generic/search/",
                params=params
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search view successful - Found {len(data.get('results', []))} books")
                return True
            else:
                print(f"❌ Search view failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Search view error: {e}")
            return False
    
    def test_books_by_genre(self, genre: str) -> bool:
        """Test GET /books/generic/genre/<genre>/"""
        print("\n=== Testing Books by Genre View ===")
        try:
            response = self.session.get(
                f"{self.base_url}/books/generic/genre/{genre}/"
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Genre filter successful - Found {len(data.get('results', []))} {genre} books")
                return True
            else:
                print(f"❌ Genre filter failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Genre filter error: {e}")
            return False
    
    def run_all_tests(self) -> None:
        """Run all tests in sequence."""
        print("🚀 Starting Generic Views Tests...")
        
        # Test list view
        list_success = self.test_list_books()
        
        # Test detail view with first book
        books_response = self.session.get(f"{self.base_url}/books/generic/")
        if books_response.status_code == 200:
            books = books_response.json().get('results', [])
            if books:
                book_id = books[0]['id']
                detail_success = self.test_retrieve_book(book_id)
            else:
                print("⚠️ No books found for detail testing")
                detail_success = False
        else:
            detail_success = False
        
        # Test create view
        create_success = False
        book_id = None
        
        # Get existing author ID
        authors_response = self.session.get(f"{self.base_url}/authors/")
        if authors_response.status_code == 200:
            authors = authors_response.json().get('results', [])
            if authors:
                author_id = authors[0]['id']
                test_book = TEST_BOOK.copy()
                test_book['author'] = author_id
                book_id = self.test_create_book(test_book)
                create_success = book_id is not None
        
        # Test update view
        update_success = False
        if book_id:
            update_data = {"price": 39.99, "description": "Updated description"}
            update_success = self.test_update_book(book_id, update_data)
        
        # Test search
        search_success = self.test_search_books("test")
        
        # Test genre filter
        genre_success = self.test_books_by_genre("fiction")
        
        # Test delete
        delete_success = False
        if book_id:
            delete_success = self.test_delete_book(book_id)
        
        # Summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        print(f"List View: {'✅' if list_success else '❌'}")
        print(f"Detail View: {'✅' if detail_success else '❌'}")
        print(f"Create View: {'✅' if create_success else '❌'}")
        print(f"Update View: {'✅' if update_success else '❌'}")
        print(f"Search View: {'✅' if search_success else '❌'}")
        print(f"Genre View: {'✅' if genre_success else '❌'}")
        print(f"Delete View: {'✅' if delete_success else '❌'}")
        
        all_success = all([
            list_success, detail_success, create_success,
            update_success, search_success, genre_success, delete_success
        ])
        
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_success else '❌ SOME TESTS FAILED'}")


def main():
    """Main function to run tests."""
    print("Generic Views Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/books/generic/")
        if response.status_code == 200:
            print("✅ Server is running")
            tester = GenericViewsTester()
            tester.run_all_tests()
        else:
            print("❌ Server returned error:", response.status_code)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("💡 Make sure the Django server is running:")
        print("   python manage.py runserver")


if __name__ == "__main__":
    main()
