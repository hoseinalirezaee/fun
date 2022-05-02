from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm as BaseAdminPasswordChangeForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _l

from users.models import User


class AdminPasswordChangeForm(BaseAdminPasswordChangeForm):
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_l("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _l("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_l("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name", "email")
    ordering = ("email",)
    readonly_fields = ["last_login", "date_joined"]
    change_password_form = AdminPasswordChangeForm
