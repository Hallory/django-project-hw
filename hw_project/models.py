from django.conf import settings
from django.db import models
from django.utils import timezone

STATUS_CHOICES = [
    ("new", "New"),
    ("in_progress", "In progress"),
    ("pending", "Pending"),
    ("blocked", "Blocked"),
    ("done", "Done"),
]


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    objects = CategoryManager()

    all_objects = models.Manager()

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["id"]

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)


class Task(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True,
    )
    categories = models.ManyToManyField("Category")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]


class SubTask(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subtasks",
        null=True,
        blank=True,
    )
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task_manager_subtask"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ["-created_at"]
