from django.urls import path
from .views import get_landsat_passes

urlpatterns = [
    path('landsat_passes/', get_landsat_passes, name='landsat_passes'),
]
