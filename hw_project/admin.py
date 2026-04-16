from django.contrib import admin

from hw_project.models import Category, SubTask, Task

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("cut_title", "status", "deadline")
    list_display_links = ("cut_title",)

    search_fields = ("title",)

    list_filter = ("status", "categories")

    list_editable = ("status",)

    list_per_page = 10

    inlines = [SubTaskInline]

    @admin.display(description="Title")
    def cut_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        else:
            return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "deadline")
    list_display_links = ("title",)

    search_fields = ("title",)

    list_filter = ("status", "task")

    list_editable = ("status",)

    autocomplete_fields = ("task",)

    list_per_page = 10

    actions = ["mark_done"]

    @admin.action(description="Mark selected subtasks as done")
    def mark_done(self, request, queryset):
        queryset.update(status="done")
        self.message_user(request, "Selected subtasks marked as done")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    ordering = ("name",)

    list_per_page = 10
