import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
django.setup()

from hw_project.models import Task, SubTask, Category


Task.objects.filter(title="Prepare presentation").delete()

print("\n--- CREATE ---")
task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare presentation for the next meeting",
    status="new",
    deadline=timezone.now() + timedelta(days=3),
)

task.categories.set(Category.objects.all())

subtask1= SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    task=task,
    status="new",
    deadline=timezone.now() + timedelta(days=2)
)

subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    task=task,
    status="new",
    deadline=timezone.now() + timedelta(days=1)
)

print("Created Task:", task)
print("Created SubTasks:", subtask1, subtask2)
print("\n--- READ ---")
new_tasks = Task.objects.filter(status="new")
print("New tasks:", list(new_tasks))

expired_done_subtasks = SubTask.objects.filter(status="done", deadline__lt=timezone.now())
print("Expired done subtasks:", list(expired_done_subtasks))
print("\n--- UPDATE ---")
task = Task.objects.get(title="Prepare presentation")
task.status = "in_progress"
task.save()
print("Updated Task status:", task.status)

subtask1 = SubTask.objects.get(title="Gather information")
subtask1.deadline = timezone.now() - timedelta(days=2)
subtask1.save()
print("Updated SubTask deadline:", subtask1.deadline)

subtask2 = SubTask.objects.get(title="Create slides")
subtask2.description = "Create and format presentation slides"
subtask2.save()
print("Updated SubTask description:", subtask2.description)

print("\n--- DELETE ---")
task = Task.objects.get(title="Prepare presentation")
print("Deleted Task:", task)
task.delete()
