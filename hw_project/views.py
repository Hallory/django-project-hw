from django.contrib.auth import authenticate
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from hw_project.models import Category, SubTask, Task

from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly
from .serializers import (
    CategorySerializer,
    RegisterSerializer,
    SubTaskCreateSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
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


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"username": user.username, "email": user.email},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        resp = Response({"access": access_token, "refresh": refresh_token})
        resp.set_cookie("access", access_token, httponly=True)
        resp.set_cookie("refresh", refresh_token, httponly=True)
        return resp


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("refresh") or request.COOKIES.get("refresh")
        if not token:
            return Response({"detail": "Refresh token required"}, status=400)
        try:
            RefreshToken(token).blacklist()
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)
        resp = Response(status=status.HTTP_205_RESET_CONTENT)
        resp.delete_cookie("access")
        resp.delete_cookie("refresh")
        return resp


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_tasks(request):
    tasks = Task.objects.filter(author=request.user)
    serializer = TaskDetailSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subtasks(request):
    subtasks = SubTask.objects.filter(author=request.user)
    serializer = SubTaskCreateSerializer(subtasks, many=True)
    return Response(serializer.data)


class SubTaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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
    permission_classes = [IsAuthorOrReadOnly]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Task.objects.all()

        status_value = self.request.query_params.get("status")
        deadline = self.request.query_params.get("deadline")

        if status_value:
            queryset = queryset.filter(status=status_value)

        if deadline:
            queryset = queryset.filter(
                deadline__date=deadline
            )  # deadline__date__lte=deadline

        return queryset


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"])
    def count_tasks(self, request, pk=None):
        category = self.get_object()

        task_count = Task.objects.filter(categories=category).count()

        return Response({"task_count": task_count, "category": category.name})


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
