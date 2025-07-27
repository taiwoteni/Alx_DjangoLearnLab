from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    
    # Fields to display in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active', 'date_joined')
    
    # Fields that can be searched
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Fields that can be filtered
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    
    # Fields to display when editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('Personal info'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
        (_('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')
    
    # Ordering
    ordering = ('username',)
    
    # Custom methods to display in the admin
    def get_full_name(self, obj):
        """Display the user's full name."""
        return obj.get_full_name() or '-'
    get_full_name.short_description = _('Full Name')
    
    def get_age(self, obj):
        """Display the user's age."""
        return obj.age or '-'
    get_age.short_description = _('Age')
    
    # Add custom methods to list display
    list_display = list_display + ('get_full_name', 'get_age')


# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Customize admin site headers
admin.site.site_header = _('Library Project Administration')
admin.site.site_title = _('Library Project Admin')
admin.site.index_title = _('Welcome to Library Project Administration')
