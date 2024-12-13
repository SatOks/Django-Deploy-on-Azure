from django.urls import path
from ..views import (
    board_list, board_create, board_detail, add_member,
    remove_member, task_create, board_update, board_delete,
    task_update, delete_task
)

urlpatterns = [
    path('', board_list, name='board_list'),
    path('board/new/', board_create, name='board_create'),
    path('board/<int:board_id>/', board_detail, name='board_detail'),
    path('board/<int:board_id>/add_member/', add_member, name='add_member'),
    path('board/<int:board_id>/remove_member/<int:user_id>/', remove_member, name='remove_member'),
    path('board/<int:board_id>/task/new/', task_create, name='task_create'),
    path('board/<int:board_id>/update/', board_update, name='board_update'),
    path('board/<int:board_id>/delete/', board_delete, name='board_delete'),
    path('task/<int:task_id>/update/', task_update, name='task_update'),
    path('task/<int:task_id>/delete/', delete_task, name='delete_task'),
]