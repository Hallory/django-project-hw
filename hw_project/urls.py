from django.urls import path
from .views import create_task,get_all_tasks,get_task_by_id, get_statistics

urlpatterns = [
    path("tasks/", create_task),
    path("tasks/", get_all_tasks),
    path("task/<int:task_id>/", get_task_by_id),
    path("statistics/", get_statistics),
    ]
