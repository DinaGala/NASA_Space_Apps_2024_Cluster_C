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

def get_new_image_time(path, row):
        try:
            start_date = '2024-01-01'
            end_date = '2024-12-31'

            landsat_collection_8 = ee.ImageCollection('LANDSAT/LC08/C02/T1').filter(ee.Filter.eq('WRS_PATH', int(path))).filter(ee.Filter.eq('WRS_ROW', int(row))).filter(ee.Filter.date(start_date, end_date))
            last_image_8 = landsat_collection_8.sort('system:time_start', False).first()

            if last_image_8:
                timestamp = last_image_8.get('system:time_start').getInfo()
                timestamp_seconds = timestamp / 1000
                last_image_datetime_8 = datetime.utcfromtimestamp(timestamp_seconds)

            landsat_collection_9 = ee.ImageCollection('LANDSAT/LC09/C02/T1').filter(ee.Filter.eq('WRS_PATH', int(path))).filter(ee.Filter.eq('WRS_ROW', int(row))).filter(ee.Filter.date(start_date, end_date))
            last_image_9 = landsat_collection_9.sort('system:time_start', False).first()
            if last_image_9:
                timestamp = last_image_9.get('system:time_start').getInfo()
                timestamp_seconds = timestamp / 1000
                last_image_datetime_9 = datetime.utcfromtimestamp(timestamp_seconds)
                
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

def postpone(user_email, next_image_time_utc)
# HERE GOES CELERY
                # Отправка уведомления
                # send_notification_email.apply_async(args=[user_email], eta=next_image)  # next_image - время отправки

                # Отправка датасета через 12 часов
                # download_and_send_dataset.apply_async(args=[user_email], eta=next_image + timedelta(hours=24))

