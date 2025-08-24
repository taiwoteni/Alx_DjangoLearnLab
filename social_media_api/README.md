# Social Media API

A Django REST API for a social media platform with posts, comments, and user following functionality.

## Features

- **User Authentication**: Token-based authentication
- **Posts**: Create, read, update, and delete posts
- **Comments**: Add comments to posts
- **User Profiles**: View user profiles
- **Following System**: Follow/unfollow users
- **Feed**: View posts from followed users
- **Search & Filter**: Search posts by title/content and filter by author

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. Run the Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Get authentication token (username & password)

### Posts
- `GET /api/posts/` - List all posts (public)
- `POST /api/posts/` - Create a new post (authenticated)
- `GET /api/posts/{id}/` - Get a specific post
- `PUT /api/posts/{id}/` - Update a post (author only)
- `DELETE /api/posts/{id}/` - Delete a post (author only)

### Comments
- `GET /api/posts/{post_id}/comments/` - List comments for a post
- `POST /api/posts/{post_id}/comments/` - Add a comment to a post
- `GET /api/comments/{id}/` - Get a specific comment
- `PUT /api/comments/{id}/` - Update a comment (author only)
- `DELETE /api/comments/{id}/` - Delete a comment (author only)

### User Profiles
- `GET /api/users/{username}/` - Get user profile
- `GET /api/users/{username}/posts/` - Get user's posts

### Following System
- `POST /api/users/{user_id}/follow/` - Follow a user
- `POST /api/users/{user_id}/unfollow/` - Unfollow a user

### Feed
- `GET /api/feed/` - Get posts from followed users (authenticated)

## Testing

### Default Admin User
- Username: admin
- Password: admin123

### Test the API
```bash
# Get authentication token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# List all posts
curl http://localhost:8000/api/posts/

# Create a post (with token)
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!"}'
```

## Technologies Used
- Django 4.2+
- Django REST Framework
- SQLite (development)
- Token Authentication
- Django Filters
- Django Search Filter
