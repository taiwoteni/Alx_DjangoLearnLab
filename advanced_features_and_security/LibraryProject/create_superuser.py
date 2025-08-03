#!/usr/bin/env python3
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        date_of_birth=date(1990, 1, 1)
    )
    print(f"Superuser '{user.username}' created successfully!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print(f"Email: {user.email}")
    print(f"Date of Birth: {user.date_of_birth}")
    print(f"Age: {user.age}")
else:
    print("Superuser 'admin' already exists.")
