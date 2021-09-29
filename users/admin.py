from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "gender",
                    "birthdate",
                    "phone",
                    # adrass
                    "buoyuser",
                    "login_method",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("buoyuser",)

    list_display = (
        "username",
        "email",
        "phone",
        # adrass
        "buoyuser",
        "is_active",
        "is_staff",
        "is_superuser",
        "login_method",
    )
