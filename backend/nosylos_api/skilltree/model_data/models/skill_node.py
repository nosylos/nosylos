import uuid

from django.db import models
from skilltree.model_data.models.skill import Skill


class SkillNodeStatus(models.TextChoices):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    ACHIEVED = "achieved"


class SkillNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parents = models.ManyToManyField(
        "SkillNode", related_name="children", blank=True
    )
    skill = models.ForeignKey(
        Skill,
        related_name="skill_nodes",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=SkillNodeStatus.choices,
        default=SkillNodeStatus.LOCKED,
    )
    # Rule to become unlocked
    need_all_parents = models.BooleanField(default=True)
    current_skill_points = models.PositiveSmallIntegerField(default=0)
    target_skill_points = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
