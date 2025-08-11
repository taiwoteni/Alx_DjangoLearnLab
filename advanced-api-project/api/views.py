"""
Advanced API Views for Book and Author Management

This module provides comprehensive REST API views for the Book and Author models
with advanced features including:
- CRUD operations
- Advanced filtering and search
- Pagination
- Custom actions
- Performance optimization
- Detailed error handling
- Comprehensive documentation
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from .models import Author
from .models import Book
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    BookListSerializer,
    AuthorDetailSerializer
)
from .filters import BookFilter, AuthorFilter
from .pagination import StandardResultsSetPagination


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Comprehensive ViewSet for Author model.
    
    Provides:
    - CRUD operations for authors
    - Custom actions for book statistics
    - Advanced filtering and search
    - Performance optimization
    - Caching
    
    list:
    Return a list of all authors with computed statistics.
    
    retrieve:
    Return detailed information about a specific author including all books.
    
    create:
    Create a new author instance.
    
    update:
    Update an existing author instance.
    
    destroy:
    Delete an author instance (cascade deletes associated books).
    
    Custom Actions:
    - books: Get all books by a specific author
    - statistics: Get comprehensive statistics for an author
    - top_rated: Get top-rated authors
    """
    
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    # Filtering and search
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = AuthorFilter
    search_fields = ['name', 'bio', 'nationality']
    ordering_fields = ['name', 'birth_date', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return AuthorDetailSerializer
        return AuthorSerializer
    
    @method_decorator(cache_page(60*15))  # Cache for 15 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """List authors with caching."""
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """
        Get all books by a specific author.
        
        Returns:
            Response: Paginated list of books by the author
        """
        author = self.get_object()
        books = author.books.all()
        
        # Apply filtering
        book_filter = BookFilter(request.GET, queryset=books)
        filtered_books = book_filter.qs
        
        # Paginate results
        page = self.paginate_queryset(filtered_books)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(filtered_books, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Get comprehensive statistics for an author.
        
        Returns:
            Response: Detailed statistics including:
                - total_books: Total number of books
                - average_rating: Average rating across all books
                - genres: Distribution of genres
                - publication_years: Distribution by year
                - price_range: Min and max prices
        """
        author = self.get_object()
        books = author.books.all()
        
        stats = {
            'total_books': books.count(),
            'average_rating': books.aggregate(
                avg_rating=Avg('rating')
            )['avg_rating'],
            'genres': list(books.values('genre').annotate(
                count=Count('id')
            ).order_by('-count')),
            'publication_years': list(books.values('publication_year').annotate(
                count=Count('id')
            ).order_by('-publication_year')),
            'price_range': books.aggregate(
                min_price=Avg('price'),
                max_price=Avg('price')
            )
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """
        Get top-rated authors based on average book ratings.
        
        Query Parameters:
            limit (int): Number of authors to return (default: 10)
        
        Returns:
            Response: List of top-rated authors with statistics
        """
        limit = int(request.query_params.get('limit', 10))
        
        authors = Author.objects.annotate(
            avg_rating=Avg('books__rating'),
            book_count=Count('books')
        ).filter(
            book_count__gt=0
        ).order_by('-avg_rating')[:limit]
        
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Author.objects.prefetch_related('books')


class BookViewSet(viewsets.ModelViewSet):
    """
    Comprehensive ViewSet for Book model.
    
    Provides:
    - CRUD operations for books
    - Custom actions for various queries
    - Advanced filtering and search
    - Performance optimization
    - Caching
    
    list:
    Return a list of all books with essential information.
    
    retrieve:
    Return detailed information about a specific book.
    
    create:
    Create a new book instance.
    
    update:
    Update an existing book instance.
    
    destroy:
    Delete a book instance.
    
    Custom Actions:
    - recent: Get recently published books
    - by_genre: Get books by genre
    - in_stock: Get available books
    - price_range: Get books within price range
    - search: Advanced search functionality
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    # Filtering and search
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = BookFilter
    search_fields = [
        'title',
        'author__name',
        'description',
        'isbn'
    ]
    ordering_fields = [
        'title',
        'publication_year',
        'rating',
        'price',
        'created_at'
    ]
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer
    
    @method_decorator(cache_page(60*5))  # Cache for 5 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """List books with caching."""
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recently published books.
        
        Query Parameters:
            years (int): Number of years to consider as recent (default: 2)
        
        Returns:
            Response: List of recent books
        """
        years = int(request.query_params.get('years', 2))
        from datetime import date
        cutoff_year = date.today().year - years
        
        recent_books = self.get_queryset().filter(
            publication_year__gte=cutoff_year
        )
        
        page = self.paginate_queryset(recent_books)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(recent_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        """
        Get books filtered by genre.
        
        Query Parameters:
            genre (str): Genre to filter by
        
        Returns:
            Response: List of books in the specified genre
        """
        genre = request.query_params.get('genre')
        if not genre:
            return Response(
                {'error': 'Genre parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = self.get_queryset().filter(genre__iexact=genre)
        
        page = self.paginate_queryset(books)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """
        Get books that are currently in stock.
        
        Returns:
            Response: List of available books
        """
        available_books = self.get_queryset().filter(in_stock=True)
        
        page = self.paginate_queryset(available_books)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(available_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def price_range(self, request):
        """
        Get books within a specific price range.
        
        Query Parameters:
            min_price (float): Minimum price (default: 0)
            max_price (float): Maximum price (default: 1000)
        
        Returns:
            Response: List of books within the price range
        """
        try:
            min_price = float(request.query_params.get('min_price', 0))
            max_price = float(request.query_params.get('max_price', 1000))
        except ValueError:
            return Response(
                {'error': 'Invalid price parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = self.get_queryset().filter(
            price__gte=min_price,
            price__lte=max_price
        )
        
        page = self.paginate_queryset(books)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search functionality.
        
        Query Parameters:
            q (str): Search query
            genre (str): Genre filter
            min_rating (float): Minimum rating
            max_rating (float): Maximum rating
            min_price (float): Minimum price
            max_price (float): Maximum price
        
        Returns:
            Response: List of matching books
        """
        queryset = self.get_queryset()
        
        # Search query
        search_query = request.query_params.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )
        
        # Genre filter
        genre = request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        
        # Rating range
        try:
            min_rating = request.query_params.get('min_rating')
            if min_rating:
                queryset = queryset.filter(rating__gte=float(min_rating))
            
            max_rating = request.query_params.get('max_rating')
            if max_rating:
                queryset = queryset.filter(rating__lte=float(max_rating))
        except ValueError:
            return Response(
                {'error': 'Invalid rating parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Price range
        try:
            min_price = request.query_params.get('min_price')
            if min_price:
                queryset = queryset.filter(price__gte=float(min_price))
            
            max_price = request.query_params.get('max_price')
            if max_price:
                queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            return Response(
                {'error': 'Invalid price parameters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BookListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = BookListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Book.objects.select_related('author')
