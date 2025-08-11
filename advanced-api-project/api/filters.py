"""
Advanced Filtering Classes for API Models

This module provides comprehensive filtering capabilities for the Book and Author models
using Django Filter backend with advanced features including:
- Range filtering for numeric fields
- Choice filtering for categorical fields
- Date filtering
- Custom filter methods
- Lookup expressions
"""

import django_filters
from django_filters import rest_framework as filters
from .models import Author, Book


class BookFilter(filters.FilterSet):
    """
    Comprehensive filter set for Book model.
    
    Provides filtering capabilities for:
    - Text fields (title, description, isbn)
    - Numeric fields (price, rating, pages, publication_year)
    - Boolean fields (in_stock)
    - Choice fields (genre)
    - Foreign key fields (author)
    - Date ranges (created_at, updated_at)
    """
    
    # Text filters
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    isbn = filters.CharFilter(lookup_expr='exact')
    
    # Numeric range filters
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    rating_min = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    
    pages_min = filters.NumberFilter(field_name='pages', lookup_expr='gte')
    pages_max = filters.NumberFilter(field_name='pages', lookup_expr='lte')
    
    # Year range filters
    publication_year_min = filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte'
    )
    publication_year_max = filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte'
    )
    
    # Choice filters
    genre = filters.ChoiceFilter(choices=Book.GENRE_CHOICES)
    
    # Boolean filters
    in_stock = filters.BooleanFilter()
    
    # Foreign key filters
    author = filters.ModelChoiceFilter(queryset=Author.objects.all())
    author_name = filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains'
    )
    
    # Date range filters
    created_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    updated_after = filters.DateTimeFilter(
        field_name='updated_at',
        lookup_expr='gte'
    )
    updated_before = filters.DateTimeFilter(
        field_name='updated_at',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'author_name',
            'isbn',
            'publication_year',
            'publication_year_min',
            'publication_year_max',
            'genre',
            'pages',
            'pages_min',
            'pages_max',
            'rating',
            'rating_min',
            'rating_max',
            'price',
            'price_min',
            'price_max',
            'in_stock',
            'created_after',
            'created_before',
            'updated_after',
            'updated_before'
        ]


class AuthorFilter(filters.FilterSet):
    """
    Comprehensive filter set for Author model.
    
    Provides filtering capabilities for:
    - Text fields (name, bio, nationality)
    - Date fields (birth_date)
    - Related book filters
    """
    
    # Text filters
    name = filters.CharFilter(lookup_expr='icontains')
    bio = filters.CharFilter(lookup_expr='icontains')
    nationality = filters.CharFilter(lookup_expr='icontains')
    
    # Date range filters
    birth_date_after = filters.DateFilter(
        field_name='birth_date',
        lookup_expr='gte'
    )
    birth_date_before = filters.DateFilter(
        field_name='birth_date',
        lookup_expr='lte'
    )
    
    # Related book filters
    has_books = filters.BooleanFilter(
        method='filter_has_books',
        label='Has books'
    )
    
    min_books = filters.NumberFilter(
        method='filter_min_books',
        label='Minimum number of books'
    )
    
    max_books = filters.NumberFilter(
        method='filter_max_books',
        label='Maximum number of books'
    )
    
    # Book-related filters
    book_genre = filters.CharFilter(
        field_name='books__genre',
        lookup_expr='iexact'
    )
    
    book_publication_year = filters.NumberFilter(
        field_name='books__publication_year',
        lookup_expr='exact'
    )
    
    book_rating_min = filters.NumberFilter(
        method='filter_book_rating_min',
        label='Minimum book rating'
    )
    
    def filter_has_books(self, queryset, name, value):
        """Filter authors based on whether they have books."""
        if value is True:
            return queryset.filter(books__isnull=False).distinct()
        elif value is False:
            return queryset.filter(books__isnull=True)
        return queryset
    
    def filter_min_books(self, queryset, name, value):
        """Filter authors with at least a certain number of books."""
        from django.db.models import Count
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__gte=value)
    
    def filter_max_books(self, queryset, name, value):
        """Filter authors with at most a certain number of books."""
        from django.db.models import Count
        return queryset.annotate(
            book_count=Count('books')
        ).filter(book_count__lte=value)
    
    def filter_book_rating_min(self, queryset, name, value):
        """Filter authors whose books have at least a certain rating."""
        from django.db.models import Avg
        return queryset.annotate(
            avg_rating=Avg('books__rating')
        ).filter(avg_rating__gte=value)
    
    class Meta:
        model = Author
        fields = [
            'name',
            'bio',
            'nationality',
            'birth_date',
            'birth_date_after',
            'birth_date_before',
            'has_books',
            'min_books',
            'max_books',
            'book_genre',
            'book_publication_year',
            'book_rating_min'
        ]
