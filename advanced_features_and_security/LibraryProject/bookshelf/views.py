from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm


# Function-based views with permission checks

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View to list all books - requires can_view permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View to create a new book - requires can_create permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """View to edit an existing book - requires can_edit permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View to delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# Class-based views with permission checks

class BookListView(PermissionRequiredMixin, ListView):
    """Class-based view to list books - requires can_view permission"""
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'


class BookCreateView(PermissionRequiredMixin, CreateView):
    """Class-based view to create books - requires can_create permission"""
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
    """Class-based view to edit books - requires can_edit permission"""
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
    """Class-based view to delete books - requires can_delete permission"""
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete'
