from .models import User, Board, Comment
#from users.serializers import UserSerializer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'user_pw'
        ]

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "author",
            "title",
            "content"
        ]

class BoardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "author",
            "title",
            "content"
        ]
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'user',
            'board',
            'content'
        ]
        
class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'user',
            'board',
            'content'
        ]