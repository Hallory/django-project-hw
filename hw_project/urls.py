from django.urls import path

from .views import (
    TaskListCreateView,
    TaskDetailView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    get_statistics,
)

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
    path("statistics/", get_statistics),
    path("subtasks/", SubTaskListCreateView.as_view()),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),
]
