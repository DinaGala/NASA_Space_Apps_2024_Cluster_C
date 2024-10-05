from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('enviar-correo-registro/', views.enviar_notificacion, name='enviar_correo-registro'),
    path('enviar-correo-landsat/', views.enviar_notificacion_landsat, name='enviar_correo_landsat'),
    path('solicitar-informacion-sin-registro/', views.solicitar_informacion_sin_registro, name='solicitar_informacion_sin_registro'),
    path('solicitar-informacion-con-registro/', views.solicitar_informacion_con_registro, name='solicitar_informacion_con_registro'),
    path('registrar-ubicacion/', views.registrar_ubicacion, name='registrar_ubicacion'),
    path('login/', views.login_view, name='login_view'),
    path('registrar-medicion/', views.registrar_medicion, name='registrar_medicion'),
    path('buscar-medicion-usuario-fecha/', views.buscar_medicion_usuario_fecha, name='buscar_medicion_por_fecha'),
]
