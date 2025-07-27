from django.contrib import admin
from .models import Book

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Enable search functionality for title and author fields
    search_fields = ('title', 'author')
    
    # Add filters in the right sidebar
    list_filter = ('publication_year', 'author')
    
    # Set the number of books displayed per page
    list_per_page = 20
    
    # Default ordering (most recent books first)
    ordering = ('-publication_year', 'title')
    
    # Fields to display in the edit form
    fields = ('title', 'author', 'publication_year')
    
    # Add help text for better user experience
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].help_text = 'Enter the full title of the book'
        form.base_fields['author'].help_text = 'Enter the author\'s full name'
        form.base_fields['publication_year'].help_text = 'Enter the year the book was published'
        return form
