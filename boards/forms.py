from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Board, Task

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': 'Required. Must be unique.',
        }

class BoardUpdateForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description']