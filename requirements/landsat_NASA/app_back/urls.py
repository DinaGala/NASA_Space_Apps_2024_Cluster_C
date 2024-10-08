from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('enviar-correo-landsat/', views.enviar_notificacion_landsat_pasando, name='enviar_correo_landsat'),
    path('enviar-correo-newinfo/', views.enviar_notificacion_newinfo, name='enviar_correo_new_info'),
    path('solicitar-informacion-sin-registro/', views.solicitar_informacion_sin_registro, name='solicitar_informacion_sin_registro'),
    path('solicitar-informacion-con-registro/', views.solicitar_informacion_con_registro, name='solicitar_informacion_con_registro'),
    path('login/', views.login_view, name='login_view'),
    path('registrar-medicion/', views.registrar_medicion, name='registrar_medicion'),
    path('buscar-medicion-usuario-fecha/', views.buscar_medicion_usuario_fecha, name='buscar_medicion_por_fecha'),
]
