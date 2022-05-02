from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _l


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields) -> "User":
        """
        Create and save a user with the given username, email, and password.
        """
        from users.services import create_user

        user = create_user(email=email, password=password, commit=False)

        is_staff = extra_fields.get("is_staff")
        is_superuser = extra_fields.get("is_superuser")

        if isinstance(is_staff, bool):
            user.is_staff = is_staff

        if isinstance(is_superuser, bool):
            user.is_superuser = is_superuser

        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        return self._create_user(email=email, password=password, is_staff=True, is_superuser=True)

    def create_user(self, email: str, password: str, **extra_fields) -> "User":
        return self._create_user(email=email, password=password)


class User(AbstractUser):
    username = None
    email = models.EmailField(_l("email address"), unique=True)

    manager = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
