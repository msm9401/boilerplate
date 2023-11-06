from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ("email",)
    # exclude = ("username",)
    model = User

    fieldsets = (
        (
            "profile",
            {
                "fields": (
                    "email",
                    "password",
                    "name",
                    "phone_number",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "phone_number", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "name", "phone_number", "is_active", "date_joined")
