from django.urls import path
from . import views

urlpatterns = [
    # Post URLs
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/user/<str:username>/', views.UserPostsView.as_view(), name='user-posts'),
    
    # Comment URLs
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    
    # Profile and Follow URLs
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile-detail'),
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow-user'),
    
    # Feed URL
    path('feed/', views.FeedView.as_view(), name='feed'),
]
