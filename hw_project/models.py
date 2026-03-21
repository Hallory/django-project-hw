from django.db import models

STATUS_CHOICES = [
    ("new", "New"),
    ("in_progress", "In progress"),
    ("pending", "Pending"),
    ("blocked", "Blocked"),
    ("done", "Done"),
]

class Task(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
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
    

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name