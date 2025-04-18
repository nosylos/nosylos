import os

from django.core.management.base import BaseCommand
from user.model_data.models.user import User


class Command(BaseCommand):
    help = "Creates super user"

    def handle(self, *args, **kwargs):
        try:
            User.objects.create_superuser(
                email="argus@nosylos.com",
                password=os.environ.get(
                    "STAGING_MASTER_USER_PASS", "v396lEuad8rEnQKw"
                ),
            )
        except Exception:
            self.stdout.write("User already exists")
