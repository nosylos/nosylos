import uuid

from django.db import models
from user.model_data.models.user import User


class Quest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="quests", on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
