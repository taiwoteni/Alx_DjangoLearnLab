"""
Django Admin Configuration for API Models

This module configures the Django admin interface for the Author and Book models,
providing comprehensive management capabilities including:
- Custom list displays
- Advanced filtering
- Search functionality
- Inline editing
- Custom actions
- Detailed form layouts
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Book


class BookInline(admin.TabularInline):
    """
    Inline configuration for Book model within Author admin.
    
    Allows quick editing of books directly from the author page.
    """
    model = Book
    extra = 1
    fields = ['title', 'publication_year', 'genre', 'rating', 'price', 'in_stock']
    readonly_fields = ['created_at']
    ordering = ['-publication_year', 'title']
    show_change_link = True
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('author')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Comprehensive admin configuration for Author model.
    
    Features:
    - Custom list display with book statistics
    - Advanced filtering and search
    - Inline book management
    - Custom actions
    - Detailed form layout
    """
    
    list_display = [
        'name',
        'nationality',
        'birth_date',
        'book_count_display',
        'average_rating_display',
        'created_at'
    ]
    
    list_filter = [
        'nationality',
        'birth_date',
        'created_at',
        'updated_at'
    ]
    
    search_fields = [
        'name',
        'bio',
        'nationality'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'book_count_display',
        'average_rating_display'
    ]
    
    ordering = ['name', '-created_at']
    
    inlines = [BookInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'bio', 'nationality', 'birth_date')
        }),
        ('Contact & Web', {
            'fields': ('website',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('book_count_display', 'average_rating_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def book_count_display(self, obj):
        """Display book count with link to filtered book list."""
        count = obj.get_book_count()
        if count > 0:
            return format_html(
                '<a href="/admin/api/book/?author__id={}">{} books</a>',
                obj.id,
                count
            )
        return "0 books"
    book_count_display.short_description = 'Total Books'
    
    def average_rating_display(self, obj):
        """Display average rating with stars."""
        rating = obj.get_average_rating()
        if rating:
            stars = '★' * int(rating) + '☆' * (5 - int(rating))
            return f"{rating:.1f}/5.0 {stars}"
        return "No ratings"
    average_rating_display.short_description = 'Average Rating'
    
    def get_queryset(self, request):
        """Optimize queryset with book count annotation."""
        return super().get_queryset(request).prefetch_related('books')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Comprehensive admin configuration for Book model.
    
    Features:
    - Custom list display with computed fields
    - Advanced filtering and search
    - Custom actions
    - Detailed form layout
    - Image preview
    """
    
    list_display = [
        'title',
        'author_link',
        'publication_year',
        'genre',
        'rating_display',
        'price',
        'in_stock',
        'book_age_display',
        'created_at'
    ]
    
    list_filter = [
        'genre',
        'publication_year',
        'in_stock',
        'rating',
        'created_at',
        'author__nationality'
    ]
    
    search_fields = [
        'title',
        'author__name',
        'isbn',
        'description'
    ]
    
    list_editable = ['price', 'in_stock']
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'book_age_display',
        'is_recent_display'
    ]
    
    ordering = ['-publication_year', 'title']
    
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'publication_year', 'genre')
        }),
        ('Content Details', {
            'fields': ('pages', 'description', 'cover_image')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'in_stock')
        }),
        ('Ratings', {
            'fields': ('rating',)
        }),
        ('Computed Fields', {
            'fields': ('book_age_display', 'is_recent_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def author_link(self, obj):
        """Display author as clickable link."""
        return format_html(
            '<a href="/admin/api/author/{}/change/">{}</a>',
            obj.author.id,
            obj.author.name
        )
    author_link.short_description = 'Author'
    
    def rating_display(self, obj):
        """Display rating with stars."""
        if obj.rating:
            stars = '★' * int(obj.rating) + '☆' * (5 - int(obj.rating))
            return f"{obj.rating}/5 {stars}"
        return "No rating"
    rating_display.short_description = 'Rating'
    
    def book_age_display(self, obj):
        """Display book age."""
        age = obj.get_age()
        if age == 0:
            return "Published this year"
        elif age == 1:
            return "1 year old"
        else:
            return f"{age} years old"
    book_age_display.short_description = 'Age'
    
    def is_recent_display(self, obj):
        """Display whether book is recent."""
        return "Yes" if obj.is_recent() else "No"
    is_recent_display.short_description = 'Recent'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('author')
