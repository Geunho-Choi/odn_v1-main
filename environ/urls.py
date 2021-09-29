from django.urls import path
from environ.views import api_view, environ_data


app_name = "environ"


urlpatterns = [
    path("", environ_data, name="env"),
    path("openapi/", api_view, name="openapi"),
]
