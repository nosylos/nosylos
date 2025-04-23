from django.contrib import admin
from plotline.model_data.models.quest import Quest
from plotline.model_data.models.task import Task


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user__email",
    )
    search_fields = ("id", "name", "user__email")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "quest__name",
    )
    search_fields = ("id", "name", "quest__id")
