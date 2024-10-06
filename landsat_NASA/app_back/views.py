from datetime import timezone
from django.shortcuts import render
import json
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
from .models import Medicion
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.shortcuts import render

from datetime import datetime, timedelta
from PIL import Image
import numpy as np
import requests
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import geopandas as gpd
from shapely.geometry import Point
import pytz
import os
import ee
import io
import math
import geopandas as gpd
from django.conf import settings
from requests.auth import HTTPBasicAuth
#from tracking.tasks import send_notification_email, download_and_send_dataset


def lista_usuarios(request):
	usuarios = Usuario.objects.all() # Obtenim tots els usuaris
	return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


#1- Solicitud notificacion Registada, el landsat pasara en X fecha y X hora
#2- El landsat esta pasando por tu zona
#3- La data esta visible, ve a verla

@csrf_exempt
def enviar_notificacion_solicitud(email, fecha, hora):
	destinatario = email
	if destinatario:
		asunto = 'Notification: request new medition'
		mensaje = f'Request has been registered. Landsat is going to pass the {fecha} at {hora}.'
		email_remitente = settings.EMAIL_HOST_USER
		try:
			send_mail(asunto, mensaje, email_remitente, [destinatario])
			return JsonResponse({'status': 'Correo enviado exitosamente'})
		except Exception as e:
			return JsonResponse({'status': 'Fallo al enviar el correo', 'error': str(e)})
	else:
		return JsonResponse({'status': 'Email no proporcionado'})


@csrf_exempt
def enviar_notificacion_newinfo(request):
	if request.method == 'POST':
		destinatario = request.POST.get('email')
		if destinatario:
			asunto = 'Notification: new data'
			mensaje = 'New data is aviable in your profile! Go to check it!'
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
def enviar_notificacion_landsat_pasando(request):
	if request.method == 'POST':
		destinatario = request.POST.get('email')
		if destinatario:
			asunto = 'Notification: landsat is passing across your ubication'
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
	return JsonResponse({"error": "Método no permitido. Usa POST."}, status=405)


def solicitar_informacion_con_registro(request):
	if request.method == 'POST':
		required_fields = ['nombre', 'password', 'email', 'longitud', 'latitud']
		for field in required_fields:
			if not request.POST.get(field):
				return JsonResponse({"error": f"El campo {field} es obligatorio."}, status=400)
	
		nombre = request.POST.get('nombre')
		password = request.POST.get('password')
		email = request.POST.get('email')
		hashed_password = make_password(password)
		longitud = float(request.POST.get('longitud'))
		latitud = float(request.POST.get('latitud'))
		path, row = get_wrs2_path_row(latitud, longitud)
		next_image_time_utc = get_new_image_time(path, row)
		next_image_time_user = get_timezone_from_coords(next_image_time_utc, latitud, longitud)

		usuario = Usuario.objects.create(
			nombre=nombre,
			password=hashed_password,
			email=email,
			longitud=longitud,
			latitud=latitud
		)
		enviar_notificacion_solicitud(email, next_image_time_utc, next_image_time_user)

		imagen = get_image(next_image_time_utc, path, row)
		
		imagen_buena = imagenDatos(returnGrid(latitud, longitud, imagen))
		print(imagen_buena)
		diccionary = retornarJSONInfo(longitud, latitud, imagen)
		print(diccionary)
		#Enviar escena y devuelve un JPG
		# Funcio que retorna un JSON de 3 indices, NDVI, Clour Cover, temperatura, NDWI
		return JsonResponse({"status": "Solicitud recibida"})
	return JsonResponse({"error": "Método no permitido. Usa POST."}, status=405)


@csrf_exempt
def login_view(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse({'status': 'Login successful'})
		else:
			return JsonResponse({'status': 'Invalid credentials'}, status=400)
	return JsonResponse({'status': 'Invalid method'}, status=405)


@login_required
def registrar_medicion(request):
	if request.method == 'POST':
		try:
			# Cargar el JSON del cuerpo de la solicitud
			data = json.loads(request.body)
			valor_R = data.get('valor_R')
			valor_G = data.get('valor_G')
			valor_B = data.get('valor_B')
			
			# Validar que todos los campos necesarios estén presentes
			if not all([valor_R, valor_G, valor_B]):
				return JsonResponse({"error": "Faltan campos requeridos"}, status=400)

			# Obtener el usuario autenticado
			usuario = request.user
			
			# Obtener la fecha y hora actual
			fecha_datetime = timezone.now()

			# Verificar si ya existe una medición para el mismo usuario y fecha (sin tiempo)
			medicion_existente = Medicion.objects.filter(usuario=usuario, fecha__date=fecha_datetime.date()).first()
			if medicion_existente:
				return JsonResponse({"status": "Ya existe una medición para esta fecha"}, status=400)

			# Crear la medición
			medicion = Medicion.objects.create(
				usuario=usuario,
				fecha=fecha_datetime,  # Usamos la fecha y hora actuales
				valor_R=valor_R,
				valor_G=valor_G,
				valor_B=valor_B
			)
			return JsonResponse({"status": "Medición registrada exitosamente", "medicion_id": medicion.id})
		
		except json.JSONDecodeError:
			return JsonResponse({"error": "JSON mal formado"}, status=400)
		except ValueError as e:
			return JsonResponse({"error": str(e)}, status=400)
	
	return JsonResponse({"error": "Método no permitido. Usa POST."}, status=405)



@login_required
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
			medicion = Medicion.objects.get(usuario=usuario, fecha__date=fecha.date()) #Busquem la medició entre la llista segons data i usuari-	
			if medicion:
				return JsonResponse({
					'status': 'Medición encontrada',
					'ubicacion': f"{usuario.latitud}, {usuario.longitud}",
					'valorRGB': {'R': medicion.valor_R, 'G': medicion.valor_G, 'B': medicion.valor_B},
					'fecha': medicion.fecha
				})
			else:
				return JsonResponse({'status': 'No se encontró ninguna medición para esa fecha'}, status=404)
		except Medicion.DoesNotExist:
			return JsonResponse({'status': 'No se encontró ninguna medición para esa fecha'}, status=404)
		except Exception as e:
			return JsonResponse({'status': 'Error en la búsqueda', 'error': str(e)}, status=500)
	return JsonResponse({'status': 'Método no permitido'}, status=405)



key_file_path = os.path.join(settings.BASE_DIR, 'data', 'ee-dinazhuzhleva-37e3107dd422.json')
#key_file_path = os.path.join(settings.PWD_DIR, 'ee-dinazhuzhleva-3f9d85c2587b.json')
credentials = ee.ServiceAccountCredentials('nasa24@ee-dinazhuzhleva.iam.gserviceaccount.com', key_file_path)
# Аутентификация
#ee.Authenticate()
# Инициализация библиотеки Earth Engine
ee.Initialize(credentials)

# Загрузите WRS-2 shapefile
wrs2_shapefile = os.path.join(settings.BASE_DIR, 'data/WRS2_descending.shp')

# Чтение shapefile в GeoDataFrame
wrs2_gdf = gpd.read_file(wrs2_shapefile)

def get_new_image_time(path, row):
		try:
			start_date = '2024-01-01'
			end_date = '2024-12-31'

			landsat_collection_8 = ee.ImageCollection('LANDSAT/LC08/C02/T1').filter(ee.Filter.eq('WRS_PATH', int(path))).filter(ee.Filter.eq('WRS_ROW', int(row))).filter(ee.Filter.date(start_date, end_date))
			last_image_8 = landsat_collection_8.sort('system:time_start', False).first()

			if last_image_8:
				timestamp = last_image_8.get('system:time_start').getInfo()
				timestamp_seconds = timestamp / 1000
				last_image_datetime_8 = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
				#last_image_datetime_8 = datetime.utcfromtimestamp(timestamp_seconds)
				

			landsat_collection_9 = ee.ImageCollection('LANDSAT/LC09/C02/T1').filter(ee.Filter.eq('WRS_PATH', int(path))).filter(ee.Filter.eq('WRS_ROW', int(row))).filter(ee.Filter.date(start_date, end_date))
			last_image_9 = landsat_collection_9.sort('system:time_start', False).first()
			if last_image_9:
				timestamp = last_image_9.get('system:time_start').getInfo()
				timestamp_seconds = timestamp / 1000
				last_image_datetime_9 = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
				#last_image_datetime_9 = datetime.utcfromtimestamp(timestamp_seconds)
				
			last_image_datetime = min(last_image_datetime_8, last_image_datetime_9)
			next_image = last_image_datetime + timedelta(days=16)
			return next_image

		except Exception as e:
			return JsonResponse({'error': str(e)}, status=500)


# Функция для поиска Path/Row по координатам
def get_wrs2_path_row(latitude, longitude):
	# Создаем точку из координат
	point = Point(longitude, latitude)
	
	# Поиск в GeoDataFrame, где точка попадает в полигоны WRS-2
	for idx, row in wrs2_gdf.iterrows():
		if row['geometry'].contains(point):
			return row['PATH'], row['ROW']
	
	# Если точка не найдена в WRS-2 зоне
	return None, None


# Function to get timezone from latitude and longitude and convert UTC timestamp to local time
def get_timezone_from_coords(next_image_utc, latitude, longitude):
	tf = TimezoneFinder()
	timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
	if timezone_str:
		local_timezone = pytz.timezone(timezone_str)
	else:
		# Fallback to UTC if no timezone found
		local_timezone = pytz.utc
	next_image_local = next_image_utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
	return next_image_local

#def postpone(user_email, next_image_time_utc)
# HERE GOES CELERY
				# Отправка уведомления
				# send_notification_email.apply_async(args=[user_email], eta=next_image)  # next_image - время отправки

				# Отправка датасета через 12 часов
				# download_and_send_dataset.apply_async(args=[user_email], eta=next_image + timedelta(hours=24))


def get_image(date, path, row):
    # Set date range for the Landsat scene
    start_date = date.strftime('%Y-%m-%d')
    end_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')

    # Filter the Landsat collection for the given path, row, and date
    landsat_collection_8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filter(ee.Filter.eq('WRS_PATH', int(path))) \
        .filter(ee.Filter.eq('WRS_ROW', int(row))) \
        .filterDate(start_date, end_date)
    
    # Get the first image (Landsat scene)
    last_image = landsat_collection_8.first()

    return last_image



# Función para calcular las nuevas coordenadas
def new_position(lat, lon, distance_km, bearing_deg):
    # Convertir grados a radianes
    lat = math.radians(lat)
    lon = math.radians(lon)
    bearing = math.radians(bearing_deg)
    
    # Radio de la Tierra en kilómetros
    R = 6371.0
    
    # Fórmulas para calcular la nueva latitud
    new_lat = math.asin(math.sin(lat) * math.cos(distance_km / R) +
                        math.cos(lat) * math.sin(distance_km / R) * math.cos(bearing))
    
    # Fórmulas para calcular la nueva longitud
    new_lon = lon + math.atan2(math.sin(bearing) * math.sin(distance_km / R) * math.cos(lat),
                               math.cos(distance_km / R) - math.sin(lat) * math.sin(new_lat))
    
    # Convertir de radianes a grados
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)
    
    return new_lat, new_lon


# Dada la latidud, la longitud y una escena retorna una matriz 3x3 de todos los datos de landsat alrededor de esa escena
def returnGrid(lon:float, lat:float, scene):
    LatSup, LonSup = new_position(lat, lon, 0.03, 45)
    LatInf, LonInf = new_position(lat, lon, -0.03, 45)
    region = ee.Geometry.BBox(LonInf, LatInf, LonSup, LatSup)
    import numpy
    url = scene.getDownloadUrl({
        'region': region,
        'scale': 20,
        'format': 'NPY'
    })
    response = requests.get(url)
    data = numpy.load(io.BytesIO(response.content))
    return data




# Dada una escena, retorna una imagen 3x3 con los píxeles RGB
def imagenDatos(data):
    print(data)
    band_blue_normalized = []
    band_green_normalized = []
    band_red_normalized = []

    for i in range(len(data)):
        listR = []
        listG = []
        listB = []
        for j in range(len(data[i])):
            listR.append((float(data[i][j][3])/20000) * 255)
            listG.append((float(data[i][j][2])/20000) * 255)
            listB.append((float(data[i][j][1])/20000) * 255)
        band_blue_normalized.append(listB)
        band_green_normalized.append(listG)
        band_red_normalized.append(listR)


    # Crear una imagen RGB combinando las bandas normalizadas
    rgb_image = np.dstack((band_red_normalized, band_green_normalized, band_blue_normalized))
    print(rgb_image)
    matriz255 = rgb_image.astype(np.uint8)
    imagen  = Image.fromarray(matriz255)
    #imagen.save('imagen_convertida.jpeg')
    return imagen



# Dada la radiancia y la emisividad retorna la temperatura (no funciona bien, hay que buscar una fórmula que funcione de verdad)
def calcularTemp(radiance:float, emis:float):
    K1 = 774.89
    K2 = 1321.08
    temperature = K2/(math.log(K1/radiance+(1)))
    LST = temperature/(emis**0.25)
    return LST

# Dadao el vector de adote
def calcularTempFromData(data):
    radiance = data[15]/65535      # Transmitancia atmosférica   
    emis = data[12]/65535     # Emisividad superficial
    return calcularTemp(radiance, emis)

# Calcula indice vegetacion mediante dato como arg
def por_vegetacionPre(data):
    nir = data[4]  # Banda 5: NIR
    red = data[3]  # Banda 4: Red
    return por_vegetacion(nir, red)
    
# Calcula indice vegetacion mediante nir y red como arg
def por_vegetacion(nir, red):
    nvdi = (nir - red)/(nir + red)
    return nvdi
# Calcula indice vegetacion mediante lon, lat, scene como arg
def calcularVegFromScene(lon, lat, scene):

    data = returnGrid(lon, lat, scene)[1][1]
    return por_vegetacionPre(data)
# Calcula indice temperatura mediante dato como arg    

def calcularTempFromScene(lon, lat, scene):
    data = returnGrid(lon, lat, scene)[1][1]
    return calcularTempFromData(data) -271 + 30

# Calcula indice humedad mediante nir, green como arg (si>0 hay humedad)    return calcularTemp(radiance, emis)-273 + 40
def humedadPre(nir, green):
    ndwi = (green-nir)/(green+nir)
    return ndwi

def humedad(data):
    nir = data[4]  # Banda 5: NIR
    green = data[2]  # Banda 3: GREEN
    return humedadPre(nir, green)

def calcularHumFromScene(lon, lat, scene):
    data = returnGrid(lon, lat, scene)[1][1]
    return humedad(data)

def calcularCloud(lon, lat, scene):
    data = returnGrid(lon, lat, scene)
    cloud = 0
    for i in range(3):
        for j in range(3):
            binario = bin(data[i][j][17])[2:]  # [2:] elimina el prefijo '0b'
            
            # Asegurarse de que la representación binaria tenga al menos 4 bits
            while len(binario) < 4:
                binario = '0' + binario  # Agregar ceros a la izquierda si es necesario
            
            # Obtener el cuarto bit (contando desde 0, así que el cuarto bit es el índice 3)
            cuarto_bit = binario[-4]  # El cuarto bit desde la derecha

            # Convertir el bit a decimal
            cuarto_bit_decimal = int(cuarto_bit)
            cloud = cloud + cuarto_bit_decimal
    return cloud/9

def retornarJSONInfo(lon, lat, scene):
    dic = {
    "temp" : calcularTempFromScene(lon,lat, scene),
    "nvdi":calcularVegFromScene(lon, lat, scene),
    "ndwi": calcularHumFromScene(lon, lat, scene),
    "cloud": calcularCloud(lon,lat,scene) #Hay que multiplicar por 100 para conseguir el %
    }
    return dic
