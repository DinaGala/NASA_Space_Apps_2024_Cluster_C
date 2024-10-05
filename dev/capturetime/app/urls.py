django.urls import path
from .views import get_landsat_passes

urlpatterns = [
	path('landsat_passes/', post, name='landsat_passes'),
]
