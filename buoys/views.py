from django.shortcuts import render
from buoys.models import Buoy
from django.views.generic import DetailView

# Create your views here.


class BuoyDetail(DetailView):

    """Buoy Detail Definition"""

    model = Buoy
