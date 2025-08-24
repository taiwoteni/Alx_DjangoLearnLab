from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'created_at', 'updated_at', 'followers_count', 'following_count']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_followers_count(self, obj):
        return obj.user.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()


class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
