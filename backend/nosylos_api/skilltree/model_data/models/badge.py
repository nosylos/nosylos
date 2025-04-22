import os
import uuid

from django.db import models
from skilltree.model_data.models.skill_node import SkillNode
from user.model_data.models.user_profile import UserProfile


def get_badge_image_path(instance, filename):
    skill_node = instance.skill_node
    return os.path.join(
        f"{skill_node.skill.user.id}-skills",
        skill_node.skill.name,
        f"{skill_node.name}-skill_node",
        "badges",
        filename,
    )


class Badge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill_node = models.OneToOneField(
        SkillNode,
        related_name="badge",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    user_profile = models.ForeignKey(
        UserProfile, related_name="badges", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    image = models.FileField(
        upload_to=get_badge_image_path, blank=True, null=True
    )
