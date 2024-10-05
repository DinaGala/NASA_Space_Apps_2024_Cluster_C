from django.urls import path
#from .views import get_landsat_passes
from .views import LandsatLastImageView

urlpatterns = [
    path('landsat-last-image/', LandsatLastImageView.as_view(), name='landsat_last_image'),
]
