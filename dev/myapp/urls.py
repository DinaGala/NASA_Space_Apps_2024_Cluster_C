from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .views import ExampleViewSet, LandsatDataView
from .views import  landsat_passes

#router = DefaultRouter()
#router.register(r'examples', ExampleViewSet)

urlpatterns = [
   # path('', include(router.urls)),
 #   path('landsat/', LandsatDataView.as_view(), name='landsat-data'),
    path('landsat_passes/', landsat_passes, name='landsat_passes'),
]
