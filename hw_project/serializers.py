from django.utils import timezone
from rest_framework import serializers

from .models import Category, SubTask, Task


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "author"]


class SubTaskSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = SubTask
        fields = ["title", "description", "status", "deadline", "author"]


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "subtasks",
            "author",
        ]


class TaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Task
        fields = ["title", "description", "status", "deadline", "created_at", "author"]

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past")
        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = SubTask
        fields = [
            "title",
            "description",
            "task",
            "status",
            "deadline",
            "created_at",
            "author",
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data["name"]).exists():
            raise serializers.ValidationError("Category already exists")
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        new_name = validated_data.get("name", instance.name)

        if Category.objects.filter(name=new_name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Category already exists")

        instance.name = new_name
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id", "is_deleted", "deleted_at"]
        read_only_fields = ["is_deleted", "deleted_at"]
