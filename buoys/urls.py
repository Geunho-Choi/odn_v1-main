from django.urls import path
from buoys.views import BuoyDetail

app_name = "buoys"

urlpatterns = [path("<int:pk>/", BuoyDetail.as_view(), name="buoys")]
