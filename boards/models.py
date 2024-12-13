from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BoardMember(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('MEMBER', 'Member'),
    ]
    
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ['board', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.board.title} ({self.role})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='TODO')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title