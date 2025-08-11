"""
Advanced API Models for Book and Author Management

This module defines the data models for a comprehensive book management system
with advanced features including:
- Author model with detailed biographical information
- Book model with comprehensive metadata
- Custom validation methods
- String representations for admin interface
- Related methods for complex queries
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class Author(models.Model):
    """
    Author model representing book authors with comprehensive information.
    
    Attributes:
        name (CharField): The author's full name
        bio (TextField): Detailed biography of the author
        birth_date (DateField): Author's date of birth
        nationality (CharField): Author's country of origin
        website (URLField): Author's official website
        created_at (DateTimeField): When the record was created
        updated_at (DateTimeField): When the record was last updated
    
    Methods:
        __str__: Returns the author's name
        get_book_count: Returns the number of books by this author
        get_latest_book: Returns the most recent book by this author
        get_average_rating: Returns average rating across all books
    """
    
    name = models.CharField(
        max_length=100,
        help_text="The author's full name",
        verbose_name="Author Name"
    )
    
    bio = models.TextField(
        blank=True,
        help_text="Detailed biography of the author",
        verbose_name="Biography"
    )
    
    birth_date = models.DateField(
        blank=True,
        null=True,
        help_text="Author's date of birth",
        verbose_name="Date of Birth"
    )
    
    nationality = models.CharField(
        max_length=50,
        blank=True,
        help_text="Author's country of origin",
        verbose_name="Nationality"
    )
    
    website = models.URLField(
        blank=True,
        help_text="Author's official website",
        verbose_name="Website"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the record was last updated"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    
    def __str__(self):
        """Return the author's name as string representation."""
        return self.name
    
    def get_book_count(self):
        """
        Get the total number of books written by this author.
        
        Returns:
            int: Number of books by this author
        """
        return self.books.count()
    
    def get_latest_book(self):
        """
        Get the most recently published book by this author.
        
        Returns:
            Book: The latest book instance or None if no books exist
        """
        return self.books.order_by('-publication_year').first()
    
    def get_average_rating(self):
        """
        Calculate the average rating across all books by this author.
        
        Returns:
            float: Average rating or 0.0 if no books have ratings
        """
        books = self.books.filter(rating__isnull=False)
        if not books.exists():
            return 0.0
        return books.aggregate(models.Avg('rating'))['rating__avg']


class Book(models.Model):
    """
    Book model representing books with comprehensive metadata.
    
    Attributes:
        title (CharField): The book's title
        author (ForeignKey): The book's author
        isbn (CharField): International Standard Book Number
        publication_year (IntegerField): Year the book was published
        genre (CharField): Book genre/category
        pages (IntegerField): Number of pages
        rating (DecimalField): Book rating (0.0 to 5.0)
        price (DecimalField): Book price
        description (TextField): Detailed book description
        cover_image (ImageField): Book cover image
        in_stock (BooleanField): Whether the book is available
        created_at (DateTimeField): When the record was created
        updated_at (DateTimeField): When the record was last updated
    
    Methods:
        __str__: Returns the book title with author
        clean: Custom validation for publication year
        is_recent: Checks if book was published in last 5 years
        get_age: Returns how many years since publication
    """
    
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('self-help', 'Self-Help'),
        ('business', 'Business'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="The book's title",
        verbose_name="Book Title"
    )
    
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The book's author"
    )
    
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="International Standard Book Number (13 digits)",
        verbose_name="ISBN"
    )
    
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(timezone.now().year)
        ],
        help_text="Year the book was published",
        verbose_name="Publication Year"
    )
    
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default='other',
        help_text="Book genre/category"
    )
    
    pages = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of pages",
        verbose_name="Page Count"
    )
    
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
        help_text="Book rating (0.0 to 5.0)"
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Book price in USD"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed book description"
    )
    
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True,
        help_text="Book cover image"
    )
    
    in_stock = models.BooleanField(
        default=True,
        help_text="Whether the book is available for purchase"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the record was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the record was last updated"
    )
    
    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        unique_together = ['title', 'author', 'publication_year']
    
    def __str__(self):
        """Return the book title with author as string representation."""
        return f"{self.title} by {self.author.name}"
    
    def clean(self):
        """
        Custom validation for the book model.
        
        Validates:
        - Publication year is not in the future
        - ISBN is exactly 13 digits
        """
        super().clean()
        
        # Validate publication year
        current_year = date.today().year
        if self.publication_year > current_year:
            raise ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Validate ISBN format
        if self.isbn and not self.isbn.isdigit():
            raise ValidationError(
                "ISBN must contain only digits."
            )
        
        if self.isbn and len(self.isbn) != 13:
            raise ValidationError(
                "ISBN must be exactly 13 digits."
            )
    
    def is_recent(self):
        """
        Check if the book was published in the last 5 years.
        
        Returns:
            bool: True if published in last 5 years, False otherwise
        """
        current_year = date.today().year
        return current_year - self.publication_year <= 5
    
    def get_age(self):
        """
        Calculate how many years have passed since publication.
        
        Returns:
            int: Number of years since publication
        """
        current_year = date.today().year
        return current_year - self.publication_year
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure clean is called.
        """
        self.full_clean()
        super().save(*args, **kwargs)
