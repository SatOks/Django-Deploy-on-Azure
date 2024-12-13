from rest_framework import serializers
from .models import Board, BoardMember, Task

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'created_at']

class BoardMemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BoardMember
        fields = ['id', 'board', 'user', 'role', 'username']

class TaskSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'board', 'status', 'created_by', 'created_by_username', 'created_at']