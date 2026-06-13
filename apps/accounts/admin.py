from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "is_active", "is_premium", "botanical_points",
    )
    list_filter = ("is_staff", "is_active", "is_premium", "groups")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {
            "fields": ("first_name", "last_name", "email", "phone"),
        }),
        ("Programme de fidélité", {
            "fields": ("is_premium", "botanical_points"),
        }),
        ("Permissions", {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions",
            ),
            "classes": ("collapse",),
        }),
        ("Dates importantes", {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",),
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2",
                "first_name", "last_name", "phone",
            ),
        }),
    )
