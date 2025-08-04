"""
Secure forms for the bookshelf application.
Implements comprehensive input validation and sanitization
to prevent XSS, SQL injection, and other security vulnerabilities.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re
from .models import Book


class BookForm(forms.ModelForm):
    """
    Secure form for book creation and editing.
    Includes input validation, sanitization, and security checks.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter book title',
                'maxlength': '200',
                'pattern': '[a-zA-Z0-9\s\-_.,:;()\'"]+',  # Basic input validation
                'title': 'Only letters, numbers, spaces, and common punctuation allowed'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter author name',
                'maxlength': '100',
                'pattern': '[a-zA-Z\s\-.\']+',  # Author name validation
                'title': 'Only letters, spaces, hyphens, periods, and apostrophes allowed'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter publication year',
                'min': '1000',
                'max': '2030',
                'title': 'Please enter a valid year between 1000 and 2030'
            }),
        }
    
    def clean_title(self):
        """Validate and sanitize book title"""
        title = self.cleaned_data.get('title')
        if title:
            # Remove potentially dangerous characters
            title = escape(title.strip())
            
            # Check for potential XSS attempts
            if re.search(r'<script|javascript:|data:|vbscript:', title, re.IGNORECASE):
                raise ValidationError('Invalid characters detected in title.')
                
            # Check length
            if len(title) > 200:
                raise ValidationError('Title is too long. Maximum 200 characters allowed.')
                
            # Check for SQL injection attempts
            sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', 'OR 1=1']
            for keyword in sql_keywords:
                if keyword.lower() in title.lower():
                    raise ValidationError(f'Invalid input detected: {keyword}')
                    
        return title
    
    def clean_author(self):
        """Validate and sanitize author name"""
        author = self.cleaned_data.get('author')
        if author:
            # Remove potentially dangerous characters
            author = escape(author.strip())
            
            # Check for potential XSS attempts
            if re.search(r'<script|javascript:|data:|vbscript:', author, re.IGNORECASE):
                raise ValidationError('Invalid characters detected in author name.')
                
            # Check length
            if len(author) > 100:
                raise ValidationError('Author name is too long. Maximum 100 characters allowed.')
                
            # Validate author name format (letters, spaces, hyphens, periods, apostrophes)
            if not re.match(r'^[a-zA-Z\s\-.\']+$', author):
                raise ValidationError('Author name contains invalid characters.')
                
        return author
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        if year:
            # Ensure year is within reasonable bounds
            if year < 1000 or year > 2030:
                raise ValidationError('Please enter a valid year between 1000 and 2030.')
                
            # Ensure year is an integer
            try:
                year = int(year)
            except (ValueError, TypeError):
                raise ValidationError('Please enter a valid year.')
                
        return year
    
    def clean(self):
        """Overall form validation"""
        cleaned_data = super().clean()
        
        # Additional security checks
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'data:',
            r'on\w+\s*=',
            r'expression\s*\(',
            r'url\s*\(',
            r'behavior\s*:',
            r'--',
            r'/\*.*\*/',
            r'union\s+select',
            r'drop\s+table',
            r'insert\s+into',
            r'delete\s+from',
            r'update\s+set',
            r'exec\s*\(',
            r'system\s*\(',
            r'passthru\s*\(',
        ]
        
        for field_name, field_value in [('title', title), ('author', author)]:
            if field_value:
                for pattern in suspicious_patterns:
                    if re.search(pattern, str(field_value), re.IGNORECASE):
                        raise ValidationError(
                            f'Potentially malicious content detected in {field_name}.'
                        )
        
        return cleaned_data


class ExampleForm(forms.Form):
    """
    Example form demonstrating security best practices.
    This form showcases various security measures including input validation,
    sanitization, and protection against common vulnerabilities.
    """
    name = forms.CharField(
        max_length=100,
        min_length=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'pattern': '[a-zA-Z\s\-.\']+',
            'title': 'Only letters, spaces, hyphens, periods, and apostrophes allowed'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    message = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message',
            'maxlength': '500'
        })
    )
    
    def clean_name(self):
        """Validate and sanitize name field"""
        name = self.cleaned_data.get('name')
        if name:
            name = escape(name.strip())
            if re.search(r'<script|javascript:|data:|vbscript:', name, re.IGNORECASE):
                raise ValidationError('Invalid characters detected in name.')
            if not re.match(r'^[a-zA-Z\s\-.\']+$', name):
                raise ValidationError('Name contains invalid characters.')
        return name
    
    def clean_message(self):
        """Validate and sanitize message field"""
        message = self.cleaned_data.get('message')
        if message:
            message = escape(message.strip())
            
            # Check for XSS attempts
            xss_patterns = [
                r'<script[^>]*>.*?</script>',
                r'javascript:',
                r'vbscript:',
                r'data:',
                r'on\w+\s*=',
            ]
            
            for pattern in xss_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    raise ValidationError('Potentially malicious content detected.')
                    
        return message
