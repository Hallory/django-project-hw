from django.contrib import admin
from hw_project.models import Task, SubTask, Category


# Задание 1:
# Добавить настройку инлайн форм для админ класса задач. При создании задачи должна появиться возможность создавать сразу и подзадачу.
# Задание 2:
# Названия задач могут быть длинными и ухудшать читаемость в Админ панели, поэтому требуется выводить в списке задач укороченный вариант – 
# первые 10 символов с добавлением «...», если название длиннее, при этом при выборе задачи для создания подзадачи должно отображаться полное название.
# Необходимо реализовать такую возможность.
# Задание 3:
# Реализовать свой action для Подзадач, который поможет выводить выбранные в Админ панели объекты в статус Done

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