#!/usr/bin/env python3
"""
Test script for Social Media API
Tests the posts and comments functionality
"""

import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
django.setup()

from django.contrib.auth.models import User
from posts.models import Post, Comment
from rest_framework.test import APIClient
from rest_framework import status

def test_api():
    print("Testing Social Media API...")
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Initialize API client
    client = APIClient()
    client.force_authenticate(user=user)
    
    print("1. Testing Post Creation...")
    
    # Test post creation
    post_data = {
        'title': 'Test Post',
        'content': 'This is a test post content.'
    }
    
    response = client.post('/api/posts/', post_data, format='json')
    if response.status_code == status.HTTP_201_CREATED:
        print("✓ Post creation successful")
        # Get the post ID from the response
        post_response = client.get('/api/posts/')
        if post_response.status_code == status.HTTP_200_OK and post_response.data['results']:
            post_id = post_response.data['results'][0]['id']
        else:
            print("✗ Could not retrieve post ID")
            return False
    else:
        print(f"✗ Post creation failed: {response.status_code}")
        return False
    
    print("2. Testing Post Retrieval...")
    
    # Test post retrieval
    response = client.get('/api/posts/')
    if response.status_code == status.HTTP_200_OK:
        print("✓ Post retrieval successful")
    else:
        print(f"✗ Post retrieval failed: {response.status_code}")
        return False
    
    print("3. Testing Comment Creation...")
    
    # Test comment creation
    comment_data = {
        'post': post_id,
        'content': 'This is a test comment.'
    }
    
    response = client.post('/api/comments/', comment_data, format='json')
    if response.status_code == status.HTTP_201_CREATED:
        print("✓ Comment creation successful")
    else:
        print(f"✗ Comment creation failed: {response.status_code}")
        return False
    
    print("4. Testing Comment Retrieval...")
    
    # Test comment retrieval
    response = client.get('/api/comments/')
    if response.status_code == status.HTTP_200_OK:
        print("✓ Comment retrieval successful")
    else:
        print(f"✗ Comment retrieval failed: {response.status_code}")
        return False
    
    print("5. Testing Filtering...")
    
    # Test filtering posts by author
    response = client.get(f'/api/posts/?author={user.id}')
    if response.status_code == status.HTTP_200_OK:
        print("✓ Post filtering successful")
    else:
        print(f"✗ Post filtering failed: {response.status_code}")
        return False
    
    print("6. Testing Search...")
    
    # Test search functionality
    response = client.get('/api/posts/?search=Test')
    if response.status_code == status.HTTP_200_OK:
        print("✓ Post search successful")
    else:
        print(f"✗ Post search failed: {response.status_code}")
        return False
    
    print("\n✓ All API tests passed successfully!")
    return True

if __name__ == '__main__':
    test_api()
