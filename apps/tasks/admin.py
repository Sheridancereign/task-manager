from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "priority", "deadline", "is_done"]
    list_filter = ["is_done", "project"]
    search_fields = ["name"]
