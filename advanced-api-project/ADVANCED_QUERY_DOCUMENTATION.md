# Advanced Query Capabilities Documentation

## Overview
The Book API provides comprehensive filtering, search, and ordering capabilities through the `/api/books/` endpoint using Django REST Framework's powerful query features.

## Available Query Parameters

### 🔍 **Filtering Options**

#### Basic Filters
- `genre` - Filter by book genre (fiction, sci-fi, technology, mystery, etc.)
- `in_stock` - Filter by availability (true/false)
- `author` - Filter by author ID
- `author_name` - Filter by author name (case-insensitive contains)

#### Range Filters
- `price_min` / `price_max` - Filter by price range
- `rating_min` / `rating_max` - Filter by rating range (0.0-5.0)
- `publication_year_min` / `publication_year_max` - Filter by publication year range
- `pages_min` / `pages_max` - Filter by page count range

#### Date Filters
- `created_after` / `created_before` - Filter by creation date
- `updated_after` / `updated_before` - Filter by last update date

### 🔎 **Search Functionality**
- `search` - Full-text search across:
  - Book title
  - Author name
  - Book description
  - ISBN

### 📊 **Ordering Options**
- `ordering` - Sort results by any field:
  - `title` / `-title` (ascending/descending)
  - `publication_year` / `-publication_year`
  - `rating` / `-rating`
  - `price` / `-price`
  - `created_at` / `-created_at`

## Usage Examples

### Basic Filtering
```
GET /api/books/?genre=technology
GET /api/books/?in_stock=true
GET /api/books/?rating_min=4.0
```

### Search
```
GET /api/books/?search=Python
GET /api/books/?search=programming
```

### Ordering
```
GET /api/books/?ordering=-rating          # Highest rated first
GET /api/books/?ordering=price           # Cheapest first
GET /api/books/?ordering=-publication_year # Newest first
```

### Combined Queries
```
# High-rated technology books, ordered by price
GET /api/books/?genre=technology&rating_min=4.0&ordering=price

# Search for Python books under $50, highest rated first
GET /api/books/?search=Python&price_max=50.00&ordering=-rating

# Recent in-stock books by specific author
GET /api/books/?publication_year_min=2020&in_stock=true&author_name=Smith
```

### Pagination
```
GET /api/books/?page=1&page_size=10
GET /api/books/?genre=fiction&page=2&page_size=5
```

## Response Format
All responses follow the standard DRF pagination format:
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python Programming Guide",
      "author": {
        "id": 2,
        "name": "Jane Doe"
      },
      "genre": "technology",
      "rating": "4.50",
      "price": "29.99",
      "in_stock": true,
      "publication_year": 2023
    }
  ]
}
```

## Implementation Details

### Filter Backend Configuration
- **DjangoFilterBackend**: Handles field-based filtering
- **SearchFilter**: Provides full-text search capabilities
- **OrderingFilter**: Enables result sorting

### Custom Filter Class
The `BookFilter` class in `api/filters.py` provides:
- Range filtering for numeric fields
- Case-insensitive text filtering
- Boolean filtering
- Foreign key relationship filtering
- Custom filter methods for complex queries

### Performance Optimizations
- Queryset optimization with `select_related('author')`
- Efficient database queries through proper indexing
- Pagination to handle large result sets
- Caching support for frequently accessed data

## Testing
Run the comprehensive test suite:
```bash
python test_advanced_queries.py
```

This validates all filtering, search, and ordering capabilities with real data scenarios.
