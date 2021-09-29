from django.contrib import admin
from environ.models import Environ

# Register your models here.


@admin.register(Environ)
class EnvironAdmin(admin.ModelAdmin):

    """Environ Admin Definition"""

    fieldsets = (
        (
            "ODN Data",
            {"fields": ("odn_data",)},
        ),
        (
            "Sea ​​Area",
            {"fields": ("ocean",)},
        ),
        (
            "Coordinates",
            {"fields": ("lat", "lng")},
        ),
        (
            "Adress",
            {"fields": ("area1", "area2", "area3", "area4")},
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
                    "measurement_time",
                )
            },
        ),
    )

    list_display = (
        "ocean",
        "area1",
        "area2",
        "area3",
        "area4",
        "temperature",
        "oxygen",
        "hydrogen",
        "salt",
        "turbidity",
        "measurement_time",
        "odn_data",
    )
    list_filter = (
        "ocean",
        "area1",
        "area2",
        "area3",
        "area4",
        "odn_data",
    )
    search_fields = ["ocean", "area1", "area2", "area3", "area4"]


# Register your models here.
