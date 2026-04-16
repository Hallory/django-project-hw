from django.urls import path

from .views import get_statistics, get_task_by_id, tasks
from hw_project.views import SubTaskListCreateView,SubTaskDetailUpdateDeleteView

urlpatterns = [
    path("tasks/", tasks),
    path("task/<int:task_id>/", get_task_by_id),
    path("statistics/", get_statistics),
    path("subtasks/", SubTaskListCreateView.as_view()),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view()),
]
