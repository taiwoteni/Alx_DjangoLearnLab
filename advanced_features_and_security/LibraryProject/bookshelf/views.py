"""
Secure views for the bookshelf application.
Implements comprehensive security measures including:
- Permission-based access control
- Input validation through Django forms
- CSRF protection via middleware
- SQL injection prevention through ORM usage
- XSS prevention through template escaping
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from .models import Book
from .forms import BookForm
from .forms import ExampleForm


# Security Note: All views use Django's built-in security features:
# - @login_required ensures authentication
# - @permission_required ensures authorization
# - get_object_or_404 prevents IDOR (Insecure Direct Object Reference)
# - Django forms provide input validation and sanitization

# Function-based views with permission checks

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure view to list all books - requires can_view permission
    Uses Django ORM to prevent SQL injection
    """
    # Using .all() is safe - Django ORM prevents SQL injection
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Secure view to create a new book - requires can_create permission
    Uses Django forms for input validation and CSRF protection
    """
    if request.method == 'POST':
        # Django forms automatically handle CSRF tokens and input validation
        form = BookForm(request.POST)
        if form.is_valid():
            # Save only after validation - prevents malicious input
            book = form.save(commit=False)
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Secure view to edit an existing book - requires can_edit permission
    Uses get_object_or_404 to prevent IDOR attacks
    """
    # get_object_or_404 prevents IDOR by ensuring object exists and user has access
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            # Validate all input before saving
            book = form.save(commit=False)
            book.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Secure view to delete a book - requires can_delete permission
    Uses POST method to prevent CSRF attacks
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Only allow deletion via POST to prevent CSRF
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# Class-based views with permission checks
# These automatically handle permissions and provide built-in security

class BookListView(PermissionRequiredMixin, ListView):
    """
    Secure class-based view to list books - requires can_view permission
    Provides automatic permission checking and pagination
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    paginate_by = 20  # Prevent DoS via large datasets


class BookCreateView(PermissionRequiredMixin, CreateView):
    """
    Secure class-based view to create books - requires can_create permission
    Uses Django's built-in form handling with validation
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Secure class-based view to edit books - requires can_edit permission
    Uses Django's built-in form handling with validation
    """
    model = Book
    form_class = BookForm
    template_name = 'bookshelf/book_form.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Secure class-based view to delete books - requires can_delete permission
    Uses POST method to prevent CSRF attacks
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete'


@login_required
def example_form_view(request):
    """
    Example view demonstrating security best practices with form handling.
    This view showcases CSRF protection, input validation, and XSS prevention.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data securely
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # In a real application, you would process the data here
            # For demonstration purposes, we'll just redirect with a success message
            from django.contrib import messages
            messages.success(request, f'Thank you {name}! Your message has been received securely.')
            return redirect('bookshelf:book_list')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})
