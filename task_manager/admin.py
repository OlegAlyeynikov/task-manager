from django.contrib import admin

from task_manager.models import Task, Worker, TaskType, Position
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "created_at",
        "deadline",
        "status",
        "priority",
        "task_type",
    ]
    list_filter = ["name", "task_type", "deadline"]
    search_fields = ["task_type", "name"]


admin.site.register(TaskType)
admin.site.register(Position)


@admin.register(Worker)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Additional info"), {"fields": ("position",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "position",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("username",)
