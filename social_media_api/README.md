# Social Media API

A Django REST Framework-based API for a social media platform with posts and comments functionality.

## Features

- **Posts Management**: Create, read, update, and delete posts
- **Comments System**: Add comments to posts with full CRUD operations
- **User Authentication**: Token-based and session authentication
- **Filtering & Search**: Filter posts by author and search by title/content
- **Pagination**: Built-in pagination for large datasets
- **RESTful Design**: Clean, RESTful API endpoints

## Project Structure

```
social_media_api/
├── posts/
│   ├── models.py          # Post and Comment models
│   ├── serializers.py     # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # URL routing
│   └── admin.py          # Django admin configuration
├── social_media_api/
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── test_api.py          # API testing script
├── manage.py            # Django management script
└── README.md            # This file
```

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install django djangorestframework django-filter
   ```

2. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Posts
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Retrieve a specific post
- `PUT /api/posts/{id}/` - Update a post
- `DELETE /api/posts/{id}/` - Delete a post

### Comments
- `GET /api/comments/` - List all comments (paginated)
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Retrieve a specific comment
- `PUT /api/comments/{id}/` - Update a comment
- `DELETE /api/comments/{id}/` - Delete a comment

### Filtering & Search
- Filter posts by author: `GET /api/posts/?author={user_id}`
- Search posts: `GET /api/posts/?search={query}`
- Order posts: `GET /api/posts/?ordering={field}`

## Authentication

The API supports two authentication methods:
- **Session Authentication**: For browser-based access
- **Token Authentication**: For programmatic access

To use token authentication:
1. Obtain a token via Django admin or create one programmatically
2. Include the token in the Authorization header: `Authorization: Token {token}`

## Data Models

### Post
- `id`: Auto-generated primary key
- `title`: Post title (required)
- `content`: Post content (required)
- `author`: Foreign key to User (auto-set)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Comment
- `id`: Auto-generated primary key
- `post`: Foreign key to Post (required)
- `author`: Foreign key to User (auto-set)
- `content`: Comment content (required)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Usage Examples

### Creating a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{"title": "My First Post", "content": "This is the content of my first post."}'
```

### Creating a Comment
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your-token-here" \
  -d '{"post": 1, "content": "Great post!"}'
```

### Filtering Posts
```bash
# Get posts by specific author
curl http://localhost:8000/api/posts/?author=1

# Search posts
curl http://localhost:8000/api/posts/?search=python

# Order posts by creation date
curl http://localhost:8000/api/posts/?ordering=-created_at
```

## Testing

Run the automated test script to validate all API endpoints:

```bash
python test_api.py
```

## API Response Format

### Successful Post Creation
```json
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content",
  "author": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "created_at": "2023-12-07T10:00:00Z",
  "updated_at": "2023-12-07T10:00:00Z",
  "comments": []
}
```

### Successful Comment Creation
```json
{
  "id": 1,
  "post": 1,
  "author": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "content": "Comment content",
  "created_at": "2023-12-07T10:30:00Z",
  "updated_at": "2023-12-07T10:30:00Z"
}
```

## Pagination

All list endpoints support pagination with the following format:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/posts/?page=2",
  "previous": null,
  "results": [...]
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found

## Development

### Adding New Features
1. Create models in `posts/models.py`
2. Add serializers in `posts/serializers.py`
3. Create views in `posts/views.py`
4. Add URL patterns in `posts/urls.py`
5. Update this README with new endpoints

### Running Tests
```bash
python manage.py test posts
```

## License

This project is open source and available under the MIT License.
