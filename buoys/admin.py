from django.contrib import admin
from buoys.models import Buoy

# Register your models here.


@admin.register(Buoy)
class BuoyAdmin(admin.ModelAdmin):

    """Buoy Admin Definition"""

    fieldsets = (
        (
            "Buoy Info",
            {
                "fields": (
                    "model_number",
                    "host",
                )
            },
        ),
        (
            "Coordinates",
            {"fields": ("lat", "lon")},
        ),
        (
            "Environ Info",
            {
                "fields": (
                    "temperature",
                    "oxygen",
                    "hydrogen",
                    "salt",
                    "turbidity",
                )
            },
        ),
        (
            "Uptime",
            {"fields": ("startup", "downtime")},
        ),
        (
            "State",
            {"fields": ("operation",)},
        ),
    )

    list_display = (
        "model_number",
        "host",
        "lat",
        "lon",
        "startup",
        "downtime",
        "operation",
    )
    list_filter = (
        "model_number",
        "lat",
        "lon",
        "startup",
        "downtime",
        "operation",
    )
    search_fields = ["model_number", "host__username", "operation"]
