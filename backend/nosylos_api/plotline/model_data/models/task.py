import uuid

from django.db import models
from plotline.model_data.models.quest import Quest
from skilltree.model_data.models.skill_node import SkillNode


class TaskStatus(models.TextChoices):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quest = models.ForeignKey(
        Quest, related_name="tasks", on_delete=models.CASCADE
    )
    skill_nodes = models.ManyToManyField(
        SkillNode, related_name="tasks", blank=True
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    priority = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    due_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
