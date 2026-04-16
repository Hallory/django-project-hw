from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

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


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all().order_by("-created_at")

        task_title = request.query_params.get("task_title")
        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)

        status_value = request.query_params.get("status")
        if status_value:
            subtasks = subtasks.filter(status=status_value)

        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)

        serializer = SubTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(
                {"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(
                {"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            subtask = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response(
                {"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND
            )

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def tasks(request):
    
    if request.method == "GET":
        tasks = Task.objects.all()
        weekday = request.query_params.get("weekday")
        if weekday:
            weekday_number = weekdays.get(weekday.lower())
            if weekday_number is None:
                return Response(
                    {"error": "Invalid weekday"}, status=status.HTTP_400_BAD_REQUEST
                )
            tasks = tasks.filter(deadline__iso_week_day=weekday_number)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_task_by_id(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data)


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
