from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Profile
from .serializers import PostSerializer, CommentSerializer, ProfileSerializer, FollowSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own posts.")
        instance.delete()


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own comments.")
        instance.delete()


class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.kwargs['username']
        return Post.objects.filter(author__username=username)


class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.profile.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, pk=user_id)
    if user_to_follow == request.user:
        return Response(
            {"error": "You cannot follow yourself"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.profile.following.add(user_to_follow)
    return Response(
        {"message": f"You are now following {user_to_follow.username}"},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, pk=user_id)
    if user_to_unfollow == request.user:
        return Response(
            {"error": "You cannot unfollow yourself"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.profile.following.remove(user_to_unfollow)
    return Response(
        {"message": f"You have unfollowed {user_to_unfollow.username}"},
        status=status.HTTP_200_OK
    )
