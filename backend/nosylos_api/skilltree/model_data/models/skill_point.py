import os
import uuid

from django.db import models
from skilltree.model_data.models.skill_node import SkillNode


def get_attachment_path(instance, filename):
    skill_node = instance.skill_node
    return os.path.join(
        f"{skill_node.skill.user.id}-skills",
        skill_node.skill.name,
        f"{skill_node.name}-skill_node",
        "skill_points",
        filename,
    )


class SkillPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill_node = models.ForeignKey(
        SkillNode, related_name="skill_points", on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    note = models.CharField(max_length=255, blank=True, null=True)
    attachment = models.FileField(
        upload_to=get_attachment_path, blank=True, null=True
    )
    points = models.PositiveSmallIntegerField(
        default=1, help_text="How many points should this count as"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
