from django.urls import path
from core.views import HomeView
from core.views import ProductView
from core.views import AboutUsView

app_name = "core"

urlpatterns = [
  path("", HomeView.as_view(), name="home"),
  path("about_us/", AboutUsView.as_view(), name="about"),
  path("iot_product/", ProductView.as_view(), name="product"),]
