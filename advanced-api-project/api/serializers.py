"""
Advanced API Serializers for Book and Author Management

This module provides comprehensive serializers for the Book and Author models
with advanced features including:
- Custom validation methods
- Nested serialization
- Field-level validation
- Object-level validation
- Read-only fields
- Custom create/update methods
- Detailed error handling
"""

from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date
from .models import Author
from .models import Book


class AuthorSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for Author model with advanced features.
    
    Provides:
    - Basic author information
    - Computed fields for book statistics
    - Custom validation for birth date
    - Nested book information (read-only)
    - Custom create/update methods
    
    Attributes:
        book_count (SerializerMethodField): Total books by author
        latest_book (SerializerMethodField): Most recent book
        average_rating (SerializerMethodField): Average rating across books
        books (SerializerMethodField): List of books (read-only)
    """
    
    book_count = serializers.SerializerMethodField()
    latest_book = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'bio',
            'birth_date',
            'nationality',
            'website',
            'book_count',
            'latest_book',
            'average_rating',
            'books',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_count', 'latest_book', 'average_rating', 'books']
    
    def get_book_count(self, obj):
        """
        Get the total number of books by this author.
        
        Args:
            obj (Author): The author instance
            
        Returns:
            int: Number of books by this author
        """
        return obj.get_book_count()
    
    def get_latest_book(self, obj):
        """
        Get the most recent book by this author.
        
        Args:
            obj (Author): The author instance
            
        Returns:
            dict: Book information or None
        """
        latest = obj.get_latest_book()
        if latest:
            return {
                'id': latest.id,
                'title': latest.title,
                'publication_year': latest.publication_year,
                'rating': float(latest.rating) if latest.rating else None
            }
        return None
    
    def get_average_rating(self, obj):
        """
        Get the average rating across all books by this author.
        
        Args:
            obj (Author): The author instance
            
        Returns:
            float: Average rating or None
        """
        return obj.get_average_rating()
    
    def get_books(self, obj):
        """
        Get a list of all books by this author (simplified view).
        
        Args:
            obj (Author): The author instance
            
        Returns:
            list: List of book dictionaries
        """
        return obj.books.values('id', 'title', 'publication_year', 'rating')
    
    def validate_birth_date(self, value):
        """
        Validate that birth date is not in the future.
        
        Args:
            value (date): The birth date to validate
            
        Returns:
            date: Validated birth date
            
        Raises:
            serializers.ValidationError: If birth date is in the future
        """
        if value and value > date.today():
            raise serializers.ValidationError(
                "Birth date cannot be in the future."
            )
        return value
    
    def validate_name(self, value):
        """
        Validate that author name is not empty and has reasonable length.
        
        Args:
            value (str): The name to validate
            
        Returns:
            str: Validated name
            
        Raises:
            serializers.ValidationError: If name is invalid
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Author name cannot be empty."
            )
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Author name must be at least 2 characters long."
            )
        
        if len(value.strip()) > 100:
            raise serializers.ValidationError(
                "Author name cannot exceed 100 characters."
            )
        
        return value.strip()
    
    def validate_website(self, value):
        """
        Validate website URL format.
        
        Args:
            value (str): The website URL to validate
            
        Returns:
            str: Validated URL
            
        Raises:
            serializers.ValidationError: If URL format is invalid
        """
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError(
                "Website must start with http:// or https://"
            )
        return value


class BookSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for Book model with advanced features.
    
    Provides:
    - Basic book information
    - Nested author information
    - Custom validation for ISBN, publication year, and rating
    - Computed fields for book age
    - Custom create/update methods
    
    Attributes:
        author_name (SerializerMethodField): Author's name
        book_age (SerializerMethodField): Years since publication
        is_recent (SerializerMethodField): Whether book is recent
    """
    
    author_name = serializers.SerializerMethodField()
    book_age = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    
    # Nested author serializer for detailed information
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'author_id',
            'author_name',
            'isbn',
            'publication_year',
            'genre',
            'pages',
            'rating',
            'price',
            'description',
            'cover_image',
            'in_stock',
            'book_age',
            'is_recent',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author_name', 'book_age', 'is_recent']
    
    def get_author_name(self, obj):
        """
        Get the author's name.
        
        Args:
            obj (Book): The book instance
            
        Returns:
            str: Author's name
        """
        return obj.author.name
    
    def get_book_age(self, obj):
        """
        Calculate how many years have passed since publication.
        
        Args:
            obj (Book): The book instance
            
        Returns:
            int: Years since publication
        """
        return obj.get_age()
    
    def get_is_recent(self, obj):
        """
        Check if the book was published in the last 5 years.
        
        Args:
            obj (Book): The book instance
            
        Returns:
            bool: True if recent, False otherwise
        """
        return obj.is_recent()
    
    def validate_isbn(self, value):
        """
        Validate ISBN format (must be 13 digits).
        
        Args:
            value (str): The ISBN to validate
            
        Returns:
            str: Validated ISBN
            
        Raises:
            serializers.ValidationError: If ISBN format is invalid
        """
        if not value:
            raise serializers.ValidationError("ISBN is required.")
        
        if not value.isdigit():
            raise serializers.ValidationError(
                "ISBN must contain only digits."
            )
        
        if len(value) != 13:
            raise serializers.ValidationError(
                "ISBN must be exactly 13 digits."
            )
        
        # Check for uniqueness
        if Book.objects.filter(isbn=value).exists():
            # Allow update for existing instance
            if self.instance and self.instance.isbn == value:
                return value
            raise serializers.ValidationError(
                "A book with this ISBN already exists."
            )
        
        return value
    
    def validate_publication_year(self, value):
        """
        Validate publication year is reasonable and not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: Validated publication year
            
        Raises:
            serializers.ValidationError: If year is invalid
        """
        current_year = timezone.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be 1000 or later."
            )
        
        return value
    
    def validate_rating(self, value):
        """
        Validate rating is between 0.0 and 5.0.
        
        Args:
            value (float): The rating to validate
            
        Returns:
            float: Validated rating
            
        Raises:
            serializers.ValidationError: If rating is invalid
        """
        if value is not None:
            if value < 0.0 or value > 5.0:
                raise serializers.ValidationError(
                    "Rating must be between 0.0 and 5.0."
                )
        return value
    
    def validate_price(self, value):
        """
        Validate price is positive.
        
        Args:
            value (float): The price to validate
            
        Returns:
            float: Validated price
            
        Raises:
            serializers.ValidationError: If price is invalid
        """
        if value < 0:
            raise serializers.ValidationError(
                "Price must be positive."
            )
        return value
    
    def validate_title(self, value):
        """
        Validate book title.
        
        Args:
            value (str): The title to validate
            
        Returns:
            str: Validated title
            
        Raises:
            serializers.ValidationError: If title is invalid
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Book title cannot be empty."
            )
        
        if len(value.strip()) < 1:
            raise serializers.ValidationError(
                "Book title must be at least 1 character long."
            )
        
        if len(value.strip()) > 200:
            raise serializers.ValidationError(
                "Book title cannot exceed 200 characters."
            )
        
        return value.strip()
    
    def validate(self, data):
        """
        Object-level validation.
        
        Args:
            data (dict): All validated data
            
        Returns:
            dict: Validated data
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        # Check for duplicate book (same title, author, and year)
        title = data.get('title')
        author = data.get('author')
        publication_year = data.get('publication_year')
        
        if title and author and publication_year:
            existing = Book.objects.filter(
                title__iexact=title,
                author=author,
                publication_year=publication_year
            )
            
            # Allow update for existing instance
            if existing.exists():
                if not self.instance or existing.first().id != self.instance.id:
                    raise serializers.ValidationError(
                        "A book with this title, author, and publication year already exists."
                    )
        
        return data
    
    def create(self, validated_data):
        """
        Create a new book instance with proper error handling.
        
        Args:
            validated_data (dict): Validated data for book creation
            
        Returns:
            Book: The created book instance
        """
        try:
            return super().create(validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                f"Error creating book: {str(e)}"
            )
    
    def update(self, instance, validated_data):
        """
        Update an existing book instance with proper error handling.
        
        Args:
            instance (Book): The book instance to update
            validated_data (dict): Validated data for update
            
        Returns:
            Book: The updated book instance
        """
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                f"Error updating book: {str(e)}"
            )


class BookListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for book list views.
    
    Provides essential book information for list endpoints.
    """
    
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author_name',
            'publication_year',
            'genre',
            'rating',
            'price',
            'in_stock'
        ]


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for author views including all books.
    
    Provides comprehensive author information with full book details.
    """
    
    books = BookListSerializer(many=True, read_only=True)
    book_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'bio',
            'birth_date',
            'nationality',
            'website',
            'book_count',
            'average_rating',
            'books',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_count', 'average_rating', 'books']
    
    def get_book_count(self, obj):
        """Get total number of books by this author."""
        return obj.get_book_count()
    
    def get_average_rating(self, obj):
        """Get average rating across all books."""
        return obj.get_average_rating()
