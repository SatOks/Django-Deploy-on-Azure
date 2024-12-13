from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ..views import BoardViewSet, TaskViewSet, BoardMemberViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='api-board')
router.register(r'tasks', TaskViewSet, basename='api-task')
router.register(r'members', BoardMemberViewSet, basename='api-member')

urlpatterns = [
    path('', include(router.urls)),
]