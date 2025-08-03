from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Book, CustomUser


class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for Book model.
    """
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    ordering = ('title',)


class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    """
    model = CustomUser
    
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'age', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_of_birth')
    
    # Fields to search in admin
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Fieldsets for the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    ordering = ('username',)


# Register the models
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
