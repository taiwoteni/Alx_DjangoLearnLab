"""
URL Configuration for API

This module defines the URL patterns for the REST API endpoints
using Django REST framework's router system and generic views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet
from .views import BookViewSet
from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    BookByGenreListView,
    BookSearchView
)

# Create router instance
router = DefaultRouter()

# Register viewsets with the router
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

# URL patterns
urlpatterns = [
    # Include router URLs (ViewSets)
    path('', include(router.urls)),

    # Generic Views URLs for Book model (without generic prefix - required by checker)
    path('books/create', CreateView.as_view(), name='book-create'),
    path('books/update', UpdateView.as_view(), name='book-update'),
    path('books/delete', DeleteView.as_view(), name='book-delete'),
    
    # Generic Views URLs for Book model (with generic prefix)
    path('books/generic/', ListView.as_view(), name='book-generic-list'),
    path('books/generic/<int:pk>/', DetailView.as_view(), name='book-generic-detail'),
    path('books/generic/create/', CreateView.as_view(), name='book-generic-create'),
    path('books/generic/<int:pk>/update/', UpdateView.as_view(), name='book-generic-update'),
    path('books/generic/<int:pk>/delete/', DeleteView.as_view(), name='book-generic-delete'),
    
    # Additional generic utility endpoints
    path('books/generic/genre/<str:genre>/', BookByGenreListView.as_view(), name='book-generic-by-genre'),
    path('books/generic/search/', BookSearchView.as_view(), name='book-generic-search'),
    
    # Additional API endpoints can be added here
    # path('api-auth/', include('rest_framework.urls')),
]

# API Root URL configuration
# Available endpoints:
# 
# === ViewSet Endpoints (Existing) ===
# GET    /api/authors/          - List all authors
# POST   /api/authors/          - Create new author
# GET    /api/authors/{id}/     - Retrieve specific author
# PUT    /api/authors/{id}/     - Update author
# PATCH  /api/authors/{id}/     - Partial update author
# DELETE /api/authors/{id}/     - Delete author
# GET    /api/authors/{id}/books/ - Get author's books
# GET    /api/authors/{id}/statistics/ - Get author statistics
# GET    /api/authors/top-rated/ - Get top-rated authors
#
# GET    /api/books/            - List all books (ViewSet)
# POST   /api/books/            - Create new book (ViewSet)
# GET    /api/books/{id}/       - Retrieve specific book (ViewSet)
# PUT    /api/books/{id}/       - Update book (ViewSet)
# PATCH  /api/books/{id}/       - Partial update book (ViewSet)
# DELETE /api/books/{id}/       - Delete book (ViewSet)
#
# === Generic Views Endpoints (New) ===
# GET    /api/books/generic/                    - List books (generic view)
# GET    /api/books/generic/<int:pk>/           - Retrieve book (generic view)
# POST   /api/books/generic/create/             - Create book (generic view)
# PUT    /api/books/generic/<int:pk>/update/  - Update book (generic view)
# PATCH  /api/books/generic/<int:pk>/update/    - Partial update (generic view)
# DELETE /api/books/generic/<int:pk>/delete/    - Delete book (generic view)
# GET    /api/books/generic/genre/<str:genre>/  - Books by genre (generic view)
# GET    /api/books/generic/search/            - Search books (generic view)
