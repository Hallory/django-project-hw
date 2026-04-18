from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics, filters

from hw_project.models import SubTask, Task

from .serializers import (
    SubTaskCreateSerializer,
    SubTaskSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskSerializer,
)
weekdays = {
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6,
        "sunday": 7,
    }

class SubTaskPagination(PageNumberPagination):
    page_size = 5


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = SubTask.objects.all()
        task_id = self.request.query_params.get("task_id")
        status_value = self.request.query_params.get("status")
        deadline = self.request.query_params.get("deadline")

        if status_value:
            queryset = queryset.filter(status=status_value)

        if deadline:
            queryset = queryset.filter(deadline__date=deadline)
            
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset
    

class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer



class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    
    def get_queryset(self):
        queryset = Task.objects.all()
        
        status_value = self.request.query_params.get("status")
        deadline = self.request.query_params.get("deadline")
        
        if status_value:
            queryset = queryset.filter(status=status_value)

        if deadline:
            queryset = queryset.filter(deadline__date=deadline) # deadline__date__lte=deadline
            
        return queryset

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    



@api_view(["GET"])
def get_statistics(request):
    tasks_by_status = (
        Task.objects.values("status")
        .annotate(count=Count("id"))
        .values("status", "count")
    )
    return Response(
        {
            "total_tasks": Task.objects.count(),
            "tasks_by_status": tasks_by_status,
            "expired_tasks": Task.objects.filter(
                Q(deadline__lt=timezone.now()) & ~Q(status="done")
            ).count(),
        }
    )
