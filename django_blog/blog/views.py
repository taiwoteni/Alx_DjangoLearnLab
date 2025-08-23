from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    UserUpdateForm
)
from .models import Post

def home_view(request):
    """Home page view showing recent posts"""
    posts = Post.objects.all().order_by('-published_date')[:5]
    context = {
        'posts': posts,
        'title': 'Home'
    }
    return render(request, 'home.html', context)

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            
            # Send welcome email
            try:
                send_mail(
                    'Welcome to Django Blog',
                    f'Hi {username},\n\nWelcome to Django Blog! Your account has been created successfully.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
            except:
                pass
            
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form, 'title': 'Register'})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, 'Invalid username or password.')
                    else:
                        messages.error(request, f'{field}: {error}')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form, 'title': 'Login'})

@login_required
def logout_view(request):
    """User logout view"""
    username = request.user.username
    logout(request)
    messages.info(request, f'You have been logged out, {username}.')
    return redirect('login')

@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get user's posts
    user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    
    context = {
        'form': form,
        'user_posts': user_posts,
        'title': 'Profile'
    }
    return render(request, 'profile.html', context)

@login_required
def change_password_view(request):
    """Change password view"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form, 'title': 'Change Password'})

@login_required
def delete_account_view(request):
    """Delete account view"""
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            username = user.username
            user.delete()
            messages.success(request, f'Your account ({username}) has been deleted.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password. Account not deleted.')
    
    return render(request, 'delete_account.html', {'title': 'Delete Account'})
