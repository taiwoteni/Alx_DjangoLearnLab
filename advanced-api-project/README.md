# Advanced Django REST API Project

A comprehensive Django REST Framework project demonstrating advanced API development with custom serializers, nested relationships, filtering, pagination, and comprehensive testing.

## 🚀 Features

- **Advanced Models**: Author and Book models with complex relationships
- **Custom Serializers**: Nested serialization with validation
- **RESTful API**: Complete CRUD operations with ViewSets
- **Filtering & Search**: Advanced filtering using django-filter
- **Pagination**: Custom pagination classes
- **Comprehensive Testing**: Unit tests, integration tests, and API tests
- **Admin Interface**: Full Django admin integration
- **Custom Endpoints**: Additional API endpoints for statistics and search

## 📋 Project Structure

```
advanced-api-project/
├── advanced_api_project/     # Django project settings
├── api/                      # Main API application
│   ├── models.py            # Author and Book models
│   ├── serializers.py       # Custom serializers with validation
│   ├── views.py            # ViewSets and custom endpoints
│   ├── urls.py             # API URL configuration
│   ├── admin.py            # Django admin configuration
│   ├── filters.py          # Custom filters
│   └── pagination.py       # Pagination classes
├── test_api.py             # Comprehensive test suite
└── README.md               # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.2+
- Django REST Framework 3.15+

### Installation Steps

1. **Clone and navigate to the project:**
```bash
cd advanced-api-project
```

2. **Install dependencies:**
```bash
pip3 install django djangorestframework django-filter
```

3. **Apply migrations:**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

4. **Create superuser:**
```bash
python3 manage.py createsuperuser
```

5. **Run tests:**
```bash
python3 test_api.py
```

6. **Start development server:**
```bash
python3 manage.py runserver
```

## 📊 API Endpoints

### Authors
- `GET /api/authors/` - List all authors
- `POST /api/authors/` - Create new author
- `GET /api/authors/{id}/` - Retrieve author details
- `PUT /api/authors/{id}/` - Update author
- `DELETE /api/authors/{id}/` - Delete author
- `GET /api/authors/{id}/books/` - Get author's books
- `GET /api/authors/{id}/statistics/` - Get author statistics
- `GET /api/authors/top-rated/` - Get top-rated authors

### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Create new book
- `GET /api/books/{id}/` - Retrieve book details
- `PUT /api/books/{id}/` - Update book
- `DELETE /api/books/{id}/` - Delete book
- `GET /api/books/search/` - Search books
- `GET /api/books/recent/` - Get recent books
- `GET /api/books/by-genre/{genre}/` - Get books by genre
- `GET /api/books/by-rating/` - Get books by rating
- `GET /api/books/by-price/` - Get books by price range
- `GET /api/books/top-rated/` - Get top-rated books
- `GET /api/books/in-stock/` - Get in-stock books

## 🔧 Models

### Author Model
- **name**: CharField - Author's full name
- **bio**: TextField - Author biography
- **nationality**: CharField - Author's nationality
- **birth_date**: DateField - Author's birth date
- **created_at**: DateTimeField - Creation timestamp
- **updated_at**: DateTimeField - Last update timestamp

### Book Model
- **title**: CharField - Book title
- **author**: ForeignKey - Relationship to Author
- **isbn**: CharField - ISBN number
- **publication_year**: IntegerField - Year of publication
- **genre**: ChoiceField - Book genre (FICTION, MYSTERY, SCIENCE, etc.)
- **pages**: IntegerField - Number of pages
- **rating**: DecimalField - Book rating (0-5)
- **price**: DecimalField - Book price
- **in_stock**: BooleanField - Stock availability
- **description**: TextField - Book description
- **created_at**: DateTimeField - Creation timestamp
- **updated_at**: DateTimeField - Last update timestamp

## 🎯 Custom Serializers

### AuthorSerializer
- Includes nested BookSerializer for related books
- Provides author statistics (total books, average rating)
- Handles complex nested data structures

### BookSerializer
- Includes nested AuthorSerializer for book author
- Custom validation for publication year (cannot be in future)
- Comprehensive field validation and error handling

## 🔍 Filtering & Search

### Available Filters
- **Authors**: name, nationality, birth_date range
- **Books**: title, author, genre, publication_year, price range, rating, in_stock
- **Search**: Full-text search on book titles and descriptions

### Usage Examples
```bash
# Get all fiction books
GET /api/books/?genre=FICTION

# Get books by price range
GET /api/books/?price_min=20&price_max=50

# Search books
GET /api/books/search/?q=django

# Get recent books
GET /api/books/recent/?years=2
```

## 📄 Pagination

- **Default**: 20 items per page
- **Customizable**: Use `page_size` parameter
- **Response format**: Includes count, next, previous, and results

## 🧪 Testing

The project includes comprehensive tests:

### Test Categories
1. **Model Tests**: Validation, relationships, string representations
2. **Serializer Tests**: Serialization, deserialization, validation
3. **API Tests**: Endpoints, CRUD operations, custom endpoints
4. **Integration Tests**: Full workflow testing

### Running Tests
```bash
# Run all tests
python3 test_api.py

# Run Django tests
python3 manage.py test api

# Run specific test
python3 manage.py test api.tests.ModelTests
```

## 🎮 Usage Examples

### Creating an Author
```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "J.K. Rowling",
    "bio": "British author, best known for Harry Potter",
    "nationality": "British",
    "birth_date": "1965-07-31"
  }'
```

### Creating a Book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Harry Potter and the Philosopher's Stone",
    "author": 1,
    "isbn": "9780747532699",
    "publication_year": 1997,
    "genre": "FICTION",
    "pages": 223,
    "rating": 4.8,
    "price": 12.99,
    "in_stock": true,
    "description": "The first book in the Harry Potter series"
  }'
```

### Getting Author with Books
```bash
curl http://localhost:8000/api/authors/1/
```

### Searching Books
```bash
curl http://localhost:8000/api/books/search/?q=harry
```

## 🔐 Authentication

- **Basic Authentication**: Username/password
- **Session Authentication**: Django sessions
- **Token Authentication**: Available via DRF

## 📈 Performance Optimizations

- **Database queries**: Optimized with select_related and prefetch_related
- **Pagination**: Efficient pagination for large datasets
- **Caching**: Ready for Redis caching implementation
- **Indexing**: Database indexes on frequently queried fields

## 🚀 Deployment

### Production Setup
1. **Environment variables**: Set DEBUG=False, configure database
2. **Static files**: Collect static files
3. **Web server**: Configure with Gunicorn/Nginx
4. **Database**: Use PostgreSQL for production

### Docker Support
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "advanced_api_project.wsgi:application"]
```

## 📚 Documentation

- **API Documentation**: Available at `/api/` (Browsable API)
- **Admin Interface**: Available at `/admin/`
- **Interactive Testing**: Use Django REST Framework's web interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
- Check the test suite: `python3 test_api.py`
- Review Django documentation: https://docs.djangoproject.com/
- Check DRF documentation: https://www.django-rest-framework.org/
