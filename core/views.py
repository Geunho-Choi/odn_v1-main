from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"
    
class AboutUsView(TemplateView):
    template_name = "about_us.html"
    
class ProductView(TemplateView):
    template_name = "iot_product.html"
