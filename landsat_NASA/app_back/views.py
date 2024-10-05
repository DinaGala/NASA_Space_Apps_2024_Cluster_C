from datetime import timezone
from django.shortcuts import render

# Create your views here.
from .models import Usuario
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import UsuarioNoRegistrados
from .models import Usuario
from django.contrib.auth.hashers import make_password
from .models import Ubicacion
from .models import Medicion
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from datetime import datetime

def lista_usuarios(request):
	usuarios = Usuario.objects.all() # Obtenim tots els usuaris
	return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


@csrf_exempt
def enviar_notificacion(request):
	if request.method == 'POST':
		destinatario = request.POST.get('email')
		if destinatario:
			asunto = 'Notificación registro de Landsat'
			mensaje = 'Usuario registrado correctamente! Gracias por la confianza'
			email_remitente = settings.EMAIL_HOST_USER

			try:
				send_mail(asunto, mensaje, email_remitente, [destinatario])
				return JsonResponse({'status': 'Correo enviado exitosamente'})
			except Exception as e:
				return JsonResponse({'status': 'Fallo al enviar el correo', 'error': str(e)})
			
		else:
			return JsonResponse({'status': 'Email no proporcionado'})
	else:
		JsonResponse({'status': 'Método no permitido'}, status=405)

#Para probarlo:
#	curl -X POST -d "email=orioljg2002@gmail.com" http://localhost:8000/app_back/enviar-correo/


@csrf_exempt
def enviar_notificacion_landsat(request):
	if request.method == 'POST':
		destinatario = request.POST.get('email')
		if destinatario:
			asunto = 'Notificación de Landsat'
			mensaje = 'El satelite landsat esta pasando por encima de tu ubicacion!'
			email_remitente = settings.EMAIL_HOST_USER

			try:
				send_mail(asunto, mensaje, email_remitente, [destinatario])
				return JsonResponse({'status': 'Correo enviado exitosamente'})
			except Exception as e:
				return JsonResponse({'status': 'Fallo al enviar el correo', 'error': str(e)})
			
		else:
			return JsonResponse({'status': 'Email no proporcionado'})
	else:
		JsonResponse({'status': 'Método no permitido'}, status=405)


def solicitar_informacion_sin_registro(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		latitud = request.POST.get('latitud')
		longitud = request.POST.get('longitud')
		
		solicitud = UsuarioNoRegistrados.objects.create(email=email, latitud=latitud, longitud=longitud)
		return JsonResponse({"status": "Solicitud recibida"})
	return render(request, 'solicitar_informacion.html')


def solicitar_informacion_con_registro(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre')
		apellidos = request.POST.get('apellidos')
		password = request.POST.get('password')
		email = request.POST.get('email')

		hashed_password = make_password(password)

		usuario = Usuario.objects.create(nombre=nombre, apellidos=apellidos, password=hashed_password, email=email)
		return JsonResponse({"status": "Solicitud recibida"})
	return render(request, 'solicitar_informacion.html')


@login_required 
def registrar_ubicacion(request):
	if request.method == 'POST':
		usuario = request.user
		latitud = request.POST.get('latitud')
		longitud = request.POST.get('longitud')
		
		if latitud is None or longitud is None:
			return JsonResponse({"status": "Latitud y longitud son requeridas"}, status=400)
		ubi_existente = Ubicacion.objects.filter(usuario=usuario, latitud=latitud, longitud=longitud).exists()
		if ubi_existente:
			return JsonResponse({"status": "Esta ubicación ya existe para el usuario"}, status=400)
		ubicacion = Ubicacion.objects.create(usuario=usuario, latitud=latitud, longitud=longitud)
		return JsonResponse({"status": "Ubicación registrada exitosamente"})

		
	return render(request, 'registrar_ubicacion.html')


@csrf_exempt
def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse({'status': 'Login successful'})
		else:
			return JsonResponse({'status': 'Invalid credentials'}, status=400)
	return JsonResponse({'status': 'Invalid method'}, status=405)



@login_required
def registrar_medicion(request):
	if request.method == 'POST':
		latitud = request.POST.get('latitud')
		longitud = request.POST.get('longitud')
		fecha = request.POST.get('fecha')  # formato 'YYYY-MM-DD HH:MM:SS
		valor_R = request.POST.get('valor_R')
		valor_G = request.POST.get('valor_G')
		valor_B = request.POST.get('valor_B')
		# Convertir la fecha de cadena a un objeto datetime
		fecha_datetime = timezone.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
		# Obtener el usuario autenticado
		usuario = request.user
		# Buscar la ubicación correspondiente a la latitud y longitud proporcionadas
		ubicacion = Ubicacion.objects.filter(usuario=usuario, latitud=latitud, longitud=longitud).first()
		if ubicacion:
			# Verificar si ya existe una medición para el mismo usuario y fecha
			medicion_existente = Medicion.objects.filter(usuario=usuario, fecha=fecha_datetime).first()
			if medicion_existente:
				return JsonResponse({"status": "Ya existe una medición para esta fecha"}, status=400)
			# Crear la medición
			medicion = Medicion.objects.create(
				usuario=usuario,
				ubicacion=ubicacion,
				fecha=fecha_datetime,
				valor_R=valor_R,
				valor_G=valor_G,
				valor_B=valor_B
			)
			return JsonResponse({"status": "Medición registrada exitosamente", "medicion_id": medicion.id})
		else:
			return JsonResponse({"status": "Ubicación no encontrada"}, status=400)

	ubicaciones = Ubicacion.objects.filter(usuario=request.user)
	return render(request, 'registrar_medicion.html', {'ubicaciones': ubicaciones})


def buscar_medicion_usuario_fecha(request):
	if request.method == 'GET':
		usuario = request.user
		fecha_str = request.GET.get('fecha')
		if not fecha_str:
			return JsonResponse({'status': 'Error: Fecha no proporcionada'}, status=400)
		try:
			fecha = datetime.strptime(fecha_str, '%Y-%m-%d')#Convertim a l'objecte
		except ValueError:
			return JsonResponse({'status': 'Error: Fecha en formato incorrecto'}, status=400)
		try:
			medicion = Medicion.objects.filter(usuario=usuario, fecha__date=fecha.date()).first() #Busquem la medició entre la llista segons data i usuari
			
			if medicion:
				return JsonResponse({
					'status': 'Medición encontrada',
					'ubicacion': f"{medicion.ubicacion.latitud}, {medicion.ubicacion.longitud}",
					'valorRGB': {'R': medicion.valor_R, 'G': medicion.valor_G, 'B': medicion.valor_B},
					'fecha': medicion.fecha
				})
			else:
				return JsonResponse({'status': 'No se encontró ninguna medición para esa fecha'}, status=404)
		except Exception as e:
			return JsonResponse({'status': 'Error en la búsqueda', 'error': str(e)}, status=500)
	return JsonResponse({'status': 'Método no permitido'}, status=405)


