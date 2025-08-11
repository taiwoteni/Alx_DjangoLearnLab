"""
Generic API Views for Book Management

This module provides generic views for the Book model using Django REST Framework's
generic views and mixins. These views offer a more granular approach compared to ViewSets
and are ideal for specific use cases where fine-grained control is needed.

Features:
- CRUD operations using generic views
- Permission-based access control
- Custom validation and error handling
- Integration with existing filtering and pagination
- Comprehensive documentation

Available Views:
- BookListView: List all books with filtering and pagination
- BookDetailView: Retrieve a single book by ID
- BookCreateView: Create a new book with validation
- BookUpdateView: Update an existing book
- BookDeleteView: Delete a book with permission checks
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer, BookListSerializer
from .filters import BookFilter
from .pagination import StandardResultsSetPagination


class BookListView(generics.ListAPIView):
    """
    List all books with filtering and pagination.
    
    This view provides a paginated list of all books with support for:
    - Filtering by genre, price range, rating, etc.
    - Search functionality across title, author, description, and ISBN
    - Ordering by various fields
    - Pagination with configurable page sizes
    
    GET /books/generic/
    Query Parameters:
        - genre: Filter by genre (e.g., fiction, mystery)
        - min_price: Minimum price filter
        - max_price: Maximum price filter
        - min_rating: Minimum rating filter
        - max_rating: Maximum rating filter
        - search: Search across title, author name, description, ISBN
        - ordering: Order by field (e.g., -publication_year, title)
        - page: Page number for pagination
        - page_size: Number of items per page
    
    Returns:
        Paginated list of books with essential information
    """
    
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    # Filtering and search configuration
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
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Book.objects.select_related('author')


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID.
    
    This view provides detailed information about a specific book including:
    - Complete book metadata
    - Author information
    - Computed fields (book age, is_recent)
    
    GET /books/generic/<int:pk>/
    
    Parameters:
        pk (int): The book's primary key/ID
    
    Returns:
        Detailed book information
    """
    
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    
    def get_queryset(self):
        """Optimize queryset with related data."""
        return Book.objects.select_related('author')


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book with validation.
    
    This view handles book creation with comprehensive validation:
    - ISBN validation (13 digits, unique)
    - Publication year validation
    - Rating validation (0.0-5.0)
    - Price validation (positive)
    - Author existence validation
    
    POST /books/generic/create/
    
    Required Fields:
        - title: Book title (max 200 chars)
        - author: Author ID (must exist)
        - isbn: 13-digit ISBN (must be unique)
        - publication_year: Year of publication
        - price: Book price (positive decimal)
    
    Optional Fields:
        - genre: Book genre (choices available)
        - pages: Number of pages
        - rating: Book rating (0.0-5.0)
        - description: Book description
        - cover_image: Book cover image
        - in_stock: Availability status
    
    Returns:
        Created book details with 201 status
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Override to add custom creation logic."""
        try:
            book = serializer.save()
            return book
        except Exception as e:
            raise ValidationError(
                f"Error creating book: {str(e)}"
            )
    
    def create(self, request, *args, **kwargs):
        """Override create to provide detailed error handling."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                book = self.perform_create(serializer)
                return Response(
                    BookSerializer(book).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    
    This view handles partial and full updates with validation:
    - All validation rules from BookCreateView apply
    - ISBN uniqueness check allows same book updates
    - Only authenticated users can update
    
    PUT /books/generic/<int:pk>/
    PATCH /books/generic/<int:pk>/
    
    Parameters:
        pk (int): The book's primary key/ID
    
    Request Body:
        Any book fields to update
    
    Returns:
        Updated book details
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        """Override to add custom update logic."""
        try:
            book = serializer.save()
            return book
        except Exception as e:
            raise ValidationError(
                f"Error updating book: {str(e)}"
            )
    
    def update(self, request, *args, **kwargs):
        """Override update to provide detailed error handling."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        
        if serializer.is_valid():
            try:
                book = self.perform_update(serializer)
                return Response(BookSerializer(book).data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book with permission checks.
    
    This view handles book deletion with:
    - Authentication required
    - Soft delete consideration (future enhancement)
    - Cascade deletion handling
    
    DELETE /books/generic/<int:pk>/
    
    Parameters:
        pk (int): The book's primary key/ID
    
    Returns:
        204 No Content on successful deletion
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def perform_destroy(self, instance):
        """Override to add custom deletion logic."""
        try:
            instance.delete()
        except Exception as e:
            return Response(
                {'error': f"Error deleting book: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to provide detailed error handling."""
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(
                {'message': 'Book deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# Additional utility views for specific use cases

class BookByGenreListView(generics.ListAPIView):
    """
    List books filtered by genre.
    
    GET /books/generic/genre/<str:genre>/
    
    Parameters:
        genre (str): The genre to filter by
    
    Returns:
        List of books in the specified genre
    """
    
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Filter books by genre from URL parameter."""
        genre = self.kwargs.get('genre', '').lower()
        return Book.objects.select_related('author').filter(
            genre__iexact=genre
        )


class BookSearchView(generics.ListAPIView):
    """
    Advanced search view for books.
    
    GET /books/generic/search/
    
    Query Parameters:
        - q: Search query (searches title, author, description, ISBN)
        - genre: Genre filter
        - min_rating: Minimum rating
        - max_rating: Maximum rating
        - min_price: Minimum price
        - max_price: Maximum price
    
    Returns:
        List of matching books
    """
    
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """Build complex search query."""
        queryset = Book.objects.select_related('author').all()
        
        # Search query
        search_query = self.request.query_params.get('q')
        if search_query:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )
        
        # Genre filter
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        
        # Rating range
        min_rating = self.request.query_params.get('min_rating')
        max_rating = self.request.query_params.get('max_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))
        if max_rating:
            queryset = queryset.filter(rating__lte=float(max_rating))
        
        # Price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(price__lte=float(max_price))
        
        return queryset
