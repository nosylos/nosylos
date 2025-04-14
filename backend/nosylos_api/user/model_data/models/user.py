import re
import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,
        is_newsletter_subscribed=True,
        password=None,
    ):
        if email is None:
            raise TypeError("User must have an email address")

        if not first_name:
            name = email.split("@")[0]
            first_name = re.split(r"\.|_", name)[0]

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            is_newsletter_subscribed=is_newsletter_subscribed,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError("Superuser requires a password.")

        user = self.create_user(
            first_name="Argus",
            last_name="Panoptes",
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


def create_uuid():
    return uuid.uuid4().hex


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(primary_key=True, default=create_uuid, max_length=35)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(db_index=True, unique=True)
    is_newsletter_subscribed = models.BooleanField(default=True)
    is_email_confirmed = models.BooleanField(default=False)

    # When user wants to delete account
    # we instead just deactivate it to preserve data
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
