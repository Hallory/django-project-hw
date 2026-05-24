from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CategoryViewSet,
    LoginView,
    LogoutView,
    RegisterView,
    SubTaskDetailUpdateDeleteView,
    SubTaskListCreateView,
    TaskDetailView,
    TaskListCreateView,
    get_statistics,
    my_subtasks,
    my_tasks,
)

router = DefaultRouter()

router.register("categories", CategoryViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version="v1",
        description="API documentation for Task Manager",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("tasks/", TaskListCreateView.as_view()),
    path("my-tasks/", my_tasks, name="my_tasks"),
    path("my-subtasks/", my_subtasks, name="my_subtasks"),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
    path("statistics/", get_statistics),
    path("subtasks/", SubTaskListCreateView.as_view()),
    path("subtasks/<int:pk>/", SubTaskDetailUpdateDeleteView.as_view()),
]
