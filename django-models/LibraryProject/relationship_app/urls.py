from django.contrib.auth import login
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import admin_view, librarian_view, member_view, add_book, BookUpdateView, BookDeleteView
from . import views
from .views import list_books
from .views import LibraryDetailView


urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', BookUpdateView.as_view(), name='edit_book'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]
