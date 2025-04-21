import uuid

from django.db import models
from user.model_data.models.user import User


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, related_name="user_profile", on_delete=models.CASCADE
    )
