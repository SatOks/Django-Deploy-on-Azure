from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Board, BoardMember, Task
from .serializers import BoardSerializer, BoardMemberSerializer, TaskSerializer
from .forms import BoardForm, TaskForm, CustomUserCreationForm, BoardUpdateForm

@login_required
def board_list(request):
    user_boards = Board.objects.filter(boardmember__user=request.user)
    return render(request, 'boards/board_list.html', {'boards': user_boards})

@login_required
def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            BoardMember.objects.create(board=board, user=request.user, role='OWNER')
            return redirect('board_detail', board_id=board.id)
    else:
        form = BoardForm()
    return render(request, 'boards/board_form.html', {'form': form})

@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if not BoardMember.objects.filter(board=board, user=request.user).exists():
        return HttpResponseForbidden()
    
    tasks = Task.objects.filter(board=board)
    members = BoardMember.objects.filter(board=board).select_related('user')
    
    return render(request, 'boards/board_detail.html', {
        'board': board,
        'tasks': tasks,
        'members': members
    })

@login_required
def board_update(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = BoardUpdateForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = BoardUpdateForm(instance=board)
    
    return render(request, 'boards/board_form.html', {'form': form, 'board': board})

@login_required
def board_delete(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        board.delete()
        return redirect('board_list')
    return redirect('board_detail', board_id=board.id)

@login_required
def add_member(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            if BoardMember.objects.filter(board=board, user=user).exists():
                messages.error(request, f'User {username} is already a member of this board.')
            else:
                BoardMember.objects.create(board=board, user=user, role='MEMBER')
                messages.success(request, f'User {username} added successfully.')
        except User.DoesNotExist:
            messages.error(request, f'User with username "{username}" not found.')
    
    return redirect('board_detail', board_id=board.id)

class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Board.objects.filter(boardmember__user=self.request.user)

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        BoardMember.objects.create(board=board, user=self.request.user, role='OWNER')

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(board__boardmember__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class BoardMemberViewSet(viewsets.ModelViewSet):
    serializer_class = BoardMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BoardMember.objects.filter(board__owner=self.request.user)

    
@login_required
def remove_member(request, board_id, user_id):
    board = get_object_or_404(Board, id=board_id)
    if board.owner != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            member = BoardMember.objects.get(board=board, user_id=user_id, role='MEMBER')
            member.delete()
            messages.success(request, 'Member removed successfully.')
        except BoardMember.DoesNotExist:
            messages.error(request, 'Member not found.')
    
    return redirect('board_detail', board_id=board.id)
    
@login_required
def task_create(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if not BoardMember.objects.filter(board=board, user=request.user).exists():
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.board = board
            task.created_by = request.user
            task.status = request.POST.get('status', 'TODO')  
            task.save()
            return redirect('board_detail', board_id=board.id)
    else:
        initial_status = request.GET.get('status', 'TODO')
        form = TaskForm(initial={'status': initial_status})
    
    return render(request, 'boards/task_form.html', {
        'form': form,
        'board': board
    })

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    board_id = task.board.id
    
    if not BoardMember.objects.filter(board=task.board, user=request.user).exists():
        return HttpResponseForbidden()
        
    if request.method == 'POST':
        task.delete()
    return redirect('board_detail', board_id=board_id)

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    board = task.board
    
    if not BoardMember.objects.filter(board=board, user=request.user).exists():
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'boards/task_form.html', {
        'form': form,
        'task': task,
        'board': board
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('board_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')