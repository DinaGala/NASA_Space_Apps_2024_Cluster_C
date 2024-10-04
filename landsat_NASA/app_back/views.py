from django.shortcuts import render

# Create your views here.
from .models import Usuario

def lista_usuarios(request):
	usuarios = Usuario.objects.all() # Obtenim tots els usuaris
	return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_overview(request):
	return Response({"message": "Hello, this is my API"})

from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def enviar_notificacion(request):
	if request.method == 'POST':
		destinatario = request.POST.get('email')
		if destinatario:
			asunto = 'Notificación de Landsat'
			mensaje = 'Landsat esta pasando sobre el area seleccionada!'
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

