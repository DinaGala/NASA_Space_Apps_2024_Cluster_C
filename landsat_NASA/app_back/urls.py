from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]

from .views import api_overview
urlpatterns = [
    path('api/', api_overview),
]

from .views import enviar_notificacion
urlpatterns = [
    path('enviar-correo/', enviar_notificacion),
]