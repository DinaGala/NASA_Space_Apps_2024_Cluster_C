from django.shortcuts import render

# Create your views here.
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
import geopandas as gpd
from django.conf import settings
from requests.auth import HTTPBasicAuth
from tracking.tasks import send_notification_email, download_and_send_dataset

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



class LandsatLastImageView(View):
    def get(self, request):
        # Получаем параметры широты и долготы от клиента
        try:
            # Получение широты и долготы из запроса
            # The same in english
            latitude = float(request.GET.get('latitude'))
            longitude = float(request.GET.get('longitude'))
            
            # Получение Path и Row через функцию
            path, row = get_wrs2_path_row(latitude, longitude)

            # Задаем диапазон поиска по дате
            start_date = '2024-01-01'
            end_date = '2024-12-31'

            # Фильтруем коллекцию Landsat 8 по path и row
            landsat_collection_8 = ee.ImageCollection('LANDSAT/LC08/C02/T1').filter(ee.Filter.eq('WRS_PATH', int(path))).filter(ee.Filter.eq('WRS_ROW', int(row))).filter(ee.Filter.date(start_date, end_date))

            # Сортируем по времени и берем самое последнее изображение
            last_image_8 = landsat_collection_8.sort('system:time_start', False).first()
             # Get the local timezone for the given coordinates
            local_timezone = get_timezone_from_coords(latitude, longitude)
            # Если изображение найдено, возвращаем его дату
            if last_image_8:
                # Получаем временную метку (timestamp) снимка
                timestamp = last_image_8.get('system:time_start').getInfo()
                timestamp_seconds = timestamp / 1000
                last_image_datetime_8 = datetime.utcfromtimestamp(timestamp_seconds)

                landsat_collection_9 = ee.ImageCollection('LANDSAT/LC09/C02/T1').filter(ee.Filter.eq('WRS_PATH', int(path))).filter(ee.Filter.eq('WRS_ROW', int(row))).filter(ee.Filter.date(start_date, end_date))
                last_image_9 = landsat_collection_9.sort('system:time_start', False).first()
                if last_image_9:
                    # Получаем временную метку (timestamp) снимка
                    timestamp = last_image_9.get('system:time_start').getInfo()
                    timestamp_seconds = timestamp / 1000
                    last_image_datetime_9 = datetime.utcfromtimestamp(timestamp_seconds)
                
                last_image_datetime = min(last_image_datetime_8, last_image_datetime_9)
                next_image = last_image_datetime + timedelta(days=16)
                    # Конвертируем временную метку в формат даты и времени
                next_image_str =  next_image.strftime('%Y-%m-%d %H:%M:%S')
                next_image_local = next_image.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                next_image_local_str = next_image_local.strftime('%Y-%m-%d %H:%M:%S')
               
 # HERE GOES CELERY
                # Отправка уведомления
                # send_notification_email.apply_async(args=[user_email], eta=next_image)  # next_image - время отправки

                # Отправка датасета через 12 часов
                # download_and_send_dataset.apply_async(args=[user_email], eta=next_image + timedelta(hours=24))
#############################################

                # Возвращаем JSON с датой и временем
                return JsonResponse({'Next image UTC': next_image_str, 'Next image local': next_image_local_str})

            else:
                return JsonResponse({'error': 'No image found for the specified scene.'}, status=404)

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


# Function to convert UTC timestamp to local time
def convert_utc_to_local(utc_time, local_timezone):
    utc_time = datetime.utcfromtimestamp(utc_time)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')


# Function to get timezone from latitude and longitude
def get_timezone_from_coords(latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    if timezone_str:
        return pytz.timezone(timezone_str)
    else:
        # Fallback to UTC if no timezone found
        return pytz.utc

def get_landsat_passes(request):
    # Get latitude and longitude from frontend (GET or POST request)
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('longitude'))
    altitude = float(request.GET.get('altitude', 100))  # Default altitude

    # Get the local timezone for the given coordinates
    local_timezone = get_timezone_from_coords(latitude, longitude)

    # Get passes for Landsat 8 and Landsat 9 using provided coordinates
    landsat_8_passes = get_satellite_passes(LANDSAT_8_NORAD_ID, latitude, longitude, altitude)

    # Extract the start and end times in local tntntgime for both satellites
    result = {
        'landsat_8': []
    }
    
    for p in landsat_8_passes:
        result['landsat_8'].append({
            'start_time': convert_utc_to_local(p['startUTC'], local_timezone),
            'end_time': convert_utc_to_local(p['endUTC'], local_timezone),
        })
    
    
    
    # Return the times as JSON response
    return JsonResponse(result)