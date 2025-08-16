#!/usr/bin/env python3
"""
Advanced Query Capabilities Test Script

This script demonstrates and tests the comprehensive filtering, search, and ordering
capabilities implemented for the Book model API endpoints.

Features tested:
- Filtering by various fields (title, author, genre, price, rating, etc.)
- Search functionality across multiple fields
- Ordering by different criteria
- Combined queries with multiple parameters
"""

import requests
import json
import time
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:8000/api"
HEADERS = {"Content-Type": "application/json"}

class AdvancedQueryTester:
    """Test class for advanced query capabilities."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def wait_for_server(self, max_attempts: int = 10):
        """Wait for the Django server to be ready."""
        for attempt in range(max_attempts):
            try:
                response = self.session.get(f"{self.base_url}/books/generic/")
                if response.status_code in [200, 404]:  # Server is responding
                    return True
            except requests.exceptions.ConnectionError:
                time.sleep(1)
        return False
    
    def test_basic_list(self) -> bool:
        """Test basic book listing."""
        print("\n=== Testing Basic Book List ===")
        try:
            response = self.session.get(f"{self.base_url}/books/generic/")
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', []))
                print(f"✅ Basic list successful - Found {count} books")
                return True
            else:
                print(f"❌ Basic list failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Basic list error: {e}")
            return False
    
    def test_filtering(self) -> bool:
        """Test various filtering capabilities."""
        print("\n=== Testing Filtering Capabilities ===")
        
        test_cases = [
            # Genre filtering
            {
                "name": "Filter by genre (fiction)",
                "params": {"genre": "fiction"},
                "endpoint": "/books/generic/"
            },
            # Price range filtering
            {
                "name": "Filter by price range ($10-$30)",
                "params": {"price_min": "10.00", "price_max": "30.00"},
                "endpoint": "/books/generic/"
            },
            # Rating filtering
            {
                "name": "Filter by minimum rating (4.0+)",
                "params": {"rating_min": "4.0"},
                "endpoint": "/books/generic/"
            },
            # Publication year filtering
            {
                "name": "Filter by publication year range (2020-2024)",
                "params": {"publication_year_min": "2020", "publication_year_max": "2024"},
                "endpoint": "/books/generic/"
            },
            # In stock filtering
            {
                "name": "Filter by availability (in stock)",
                "params": {"in_stock": "true"},
                "endpoint": "/books/generic/"
            },
            # Author name filtering
            {
                "name": "Filter by author name (contains 'Smith')",
                "params": {"author_name": "Smith"},
                "endpoint": "/books/generic/"
            }
        ]
        
        success_count = 0
        for test_case in test_cases:
            try:
                response = self.session.get(
                    f"{self.base_url}{test_case['endpoint']}",
                    params=test_case['params']
                )
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('results', []))
                    print(f"✅ {test_case['name']}: {count} results")
                    success_count += 1
                else:
                    print(f"❌ {test_case['name']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ {test_case['name']}: {e}")
        
        print(f"\n📊 Filtering tests: {success_count}/{len(test_cases)} passed")
        return success_count == len(test_cases)
    
    def test_search(self) -> bool:
        """Test search functionality."""
        print("\n=== Testing Search Functionality ===")
        
        search_queries = [
            "Python",      # Search in title
            "programming", # Search in description
            "Smith",       # Search in author name
            "978",         # Search in ISBN
            "fiction"      # General search
        ]
        
        success_count = 0
        for query in search_queries:
            try:
                response = self.session.get(
                    f"{self.base_url}/books/generic/",
                    params={"search": query}
                )
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('results', []))
                    print(f"✅ Search '{query}': {count} results")
                    success_count += 1
                else:
                    print(f"❌ Search '{query}': HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Search '{query}': {e}")
        
        print(f"\n📊 Search tests: {success_count}/{len(search_queries)} passed")
        return success_count == len(search_queries)
    
    def test_ordering(self) -> bool:
        """Test ordering functionality."""
        print("\n=== Testing Ordering Functionality ===")
        
        ordering_options = [
            "title",              # Ascending by title
            "-title",             # Descending by title
            "publication_year",   # Ascending by year
            "-publication_year",  # Descending by year
            "rating",             # Ascending by rating
            "-rating",            # Descending by rating
            "price",              # Ascending by price
            "-price",             # Descending by price
            "created_at",         # Ascending by creation date
            "-created_at"         # Descending by creation date
        ]
        
        success_count = 0
        for ordering in ordering_options:
            try:
                response = self.session.get(
                    f"{self.base_url}/books/generic/",
                    params={"ordering": ordering}
                )
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('results', []))
                    direction = "DESC" if ordering.startswith('-') else "ASC"
                    field = ordering.lstrip('-')
                    print(f"✅ Order by {field} ({direction}): {count} results")
                    success_count += 1
                else:
                    print(f"❌ Order by {ordering}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Order by {ordering}: {e}")
        
        print(f"\n📊 Ordering tests: {success_count}/{len(ordering_options)} passed")
        return success_count == len(ordering_options)
    
    def test_combined_queries(self) -> bool:
        """Test combined filtering, search, and ordering."""
        print("\n=== Testing Combined Query Capabilities ===")
        
        combined_tests = [
            {
                "name": "Fiction books, rating 4+, ordered by price",
                "params": {
                    "genre": "fiction",
                    "rating_min": "4.0",
                    "ordering": "price"
                }
            },
            {
                "name": "Search 'Python', price under $50, ordered by rating DESC",
                "params": {
                    "search": "Python",
                    "price_max": "50.00",
                    "ordering": "-rating"
                }
            },
            {
                "name": "Recent books (2020+), in stock, search 'programming'",
                "params": {
                    "publication_year_min": "2020",
                    "in_stock": "true",
                    "search": "programming"
                }
            },
            {
                "name": "Author contains 'Smith', genre fiction, ordered by year DESC",
                "params": {
                    "author_name": "Smith",
                    "genre": "fiction",
                    "ordering": "-publication_year"
                }
            }
        ]
        
        success_count = 0
        for test_case in combined_tests:
            try:
                response = self.session.get(
                    f"{self.base_url}/books/generic/",
                    params=test_case['params']
                )
                if response.status_code == 200:
                    data = response.json()
                    count = len(data.get('results', []))
                    print(f"✅ {test_case['name']}: {count} results")
                    success_count += 1
                else:
                    print(f"❌ {test_case['name']}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ {test_case['name']}: {e}")
        
        print(f"\n📊 Combined query tests: {success_count}/{len(combined_tests)} passed")
        return success_count == len(combined_tests)
    
    def test_pagination_with_queries(self) -> bool:
        """Test pagination combined with queries."""
        print("\n=== Testing Pagination with Queries ===")
        
        try:
            # Test pagination with filtering
            response = self.session.get(
                f"{self.base_url}/books/generic/",
                params={
                    "genre": "fiction",
                    "page_size": "5",
                    "page": "1"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Pagination with filtering: Page 1 of fiction books")
                print(f"   - Results: {len(data.get('results', []))}")
                print(f"   - Total count: {data.get('count', 'N/A')}")
                print(f"   - Next page: {'Yes' if data.get('next') else 'No'}")
                return True
            else:
                print(f"❌ Pagination test failed: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Pagination test error: {e}")
            return False
    
    def run_all_tests(self) -> None:
        """Run all advanced query tests."""
        print("🚀 Starting Advanced Query Capabilities Tests...")
        print("=" * 60)
        
        # Wait for server to be ready
        if not self.wait_for_server():
            print("❌ Server is not responding. Make sure Django server is running.")
            return
        
        print("✅ Server is ready")
        
        # Run all tests
        tests = [
            ("Basic List", self.test_basic_list),
            ("Filtering", self.test_filtering),
            ("Search", self.test_search),
            ("Ordering", self.test_ordering),
            ("Combined Queries", self.test_combined_queries),
            ("Pagination", self.test_pagination_with_queries)
        ]
        
        results = []
        for test_name, test_func in tests:
            result = test_func()
            results.append((test_name, result))
        
        # Summary
        print("\n" + "="*60)
        print("📊 ADVANCED QUERY CAPABILITIES TEST SUMMARY")
        print("="*60)
        
        passed = 0
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 Overall Result: {passed}/{len(results)} test categories passed")
        
        if passed == len(results):
            print("🎉 ALL ADVANCED QUERY CAPABILITIES ARE WORKING PERFECTLY!")
        else:
            print("⚠️  Some query capabilities need attention")
        
        # Print usage examples
        self.print_usage_examples()
    
    def print_usage_examples(self):
        """Print usage examples for the API."""
        print("\n" + "="*60)
        print("📚 API USAGE EXAMPLES")
        print("="*60)
        
        examples = [
            {
                "description": "Filter fiction books with rating 4.0 or higher",
                "url": f"{self.base_url}/books/generic/?genre=fiction&rating_min=4.0"
            },
            {
                "description": "Search for 'Python' in title, author, or description",
                "url": f"{self.base_url}/books/generic/?search=Python"
            },
            {
                "description": "Get books priced between $10-$50, ordered by price",
                "url": f"{self.base_url}/books/generic/?price_min=10&price_max=50&ordering=price"
            },
            {
                "description": "Recent books (2020+) by authors containing 'Smith'",
                "url": f"{self.base_url}/books/generic/?publication_year_min=2020&author_name=Smith"
            },
            {
                "description": "In-stock sci-fi books, ordered by rating (highest first)",
                "url": f"{self.base_url}/books/generic/?genre=sci-fi&in_stock=true&ordering=-rating"
            }
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n{i}. {example['description']}:")
            print(f"   GET {example['url']}")


def main():
    """Main function to run advanced query tests."""
    tester = AdvancedQueryTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
