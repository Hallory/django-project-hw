from django.urls import path
from .views import tasks,get_task_by_id, get_statistics

urlpatterns = [
    path("tasks/", tasks),
    path("task/<int:task_id>/", get_task_by_id),
    path("statistics/", get_statistics),
    ]
