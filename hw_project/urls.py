from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    TaskListCreateView,
    TaskDetailView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    get_statistics,
    CategoryViewSet,
)
router = DefaultRouter()

router.register("categories", CategoryViewSet)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tasks/", TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
    path("statistics/", get_statistics),
    path("subtasks/", SubTaskListCreateView.as_view()),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),
]
