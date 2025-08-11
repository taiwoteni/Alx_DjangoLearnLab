"""
URL Configuration for API

This module defines the URL patterns for the REST API endpoints
using Django REST framework's router system.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet

# Create router instance
router = DefaultRouter()

# Register viewsets with the router
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

# URL patterns
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Additional API endpoints can be added here
    # path('api-auth/', include('rest_framework.urls')),
]

# API Root URL configuration
# This will be automatically handled by the DefaultRouter
# Available endpoints:
# GET    /api/authors/          - List all authors
# POST   /api/authors/          - Create new author
# GET    /api/authors/{id}/     - Retrieve specific author
# PUT    /api/authors/{id}/     - Update author
# PATCH  /api/authors/{id}/     - Partial update author
# DELETE /api/authors/{id}/     - Delete author
# GET    /api/authors/{id}/books/ - Get author's books
# GET    /api/authors/{id}/statistics/ - Get author statistics
# GET    /api/authors/top-rated/ - Get top-rated authors

# GET    /api/books/            - List all books
# POST   /api/books/            - Create new book
# GET    /api/books/{id}/       - Retrieve specific book
# PUT    /api/books/{id}/       - Update book
# PATCH  /api/books/{id}/       - Partial update book
# DELETE /api/books/{id}/       - Delete book
# GET    /api/books/search/     - Search books with filters
# GET    /api/books/by-genre/{genre}/ - Get books by genre
# GET    /api/books/by-rating/  - Get books by rating range
# GET    /api/books/by-price/   - Get books by price range
# GET    /api/books/top-rated/  - Get top-rated books
# GET    /api/books/in-stock/   - Get in-stock books
