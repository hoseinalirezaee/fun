from typing import Optional

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from users.models import User


def create_user(
    email: str,
    password: str,
    perform_password_validation: bool = False,
    commit: bool = True,
    using: Optional[str] = None,
) -> User:
    if User.objects.filter(email=email).exists():
        raise ValidationError(message=_("A user has already registered with this email."))

    user = User(email=email)
    if perform_password_validation:
        validate_password(password=password, user=user)
    user.set_password(password)

    if commit:
        user.save(using=using)

    return user
