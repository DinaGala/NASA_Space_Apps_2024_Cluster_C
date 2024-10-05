import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Example
from .serializers import ExampleSerializer
import json
from django.http import JsonResponse

import requests
from django.http import JsonResponse
from django.shortcuts import render

# API Key от N2YO (зарегистрируйтесь и получите ключ)
API_KEY = '8VBB7W-PHAH5H-2K2JR9-5CIX'

# ID спутника Landsat 8
LANDSAT_8_NORAD_ID = 39084

# Координаты местоположения
LATITUDE = 55.7558  # Пример: Москва
LONGITUDE = 37.6173
ALTITUDE = 100  # Примерная высота над уровнем моря в метрах

def landsat_passes(request):
    # Параметры запроса к API
    url = f'http://api.n2yo.com/rest/v1/satellite/visualpasses/{LANDSAT_8_NORAD_ID}/{LATITUDE}/{LONGITUDE}/{ALTITUDE}/10/10/&apiKey={API_KEY}'
    
    # Отправка запроса
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'No API data'}, status=500)


class LandsatDataView(APIView):
    def get(self, request, *args, **kwargs):
        # Пример параметров для API Landsat
        longitude = request.query_params.get('longitude', None)
        latitude = request.query_params.get('latitude', None)

        if longitude is None or latitude is None:
            return Response({'error': 'Longitude and Latitude are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Пример URL для запроса данных к API (например, USGS или Google Earth Engine)
        api_url = 'https://earthexplorer.usgs.gov/inventory/json/v/1.4.1/'  # Примерный URL, замените на правильный

        # Параметры для запроса данных от Landsat API
        params = {
            'longitude': longitude,
            'latitude': latitude,
            'format': 'json',
            'cloud_cover_max': 10,  # например, фильтр по облачности
        }

        # Отправляем запрос
        try:
            response = requests.get(api_url, params=params)

            # Проверяем успешность запроса
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to retrieve data from Landsat API'}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#class ExampleViewSet(viewsets.ModelViewSet):
#    queryset = Example.objects.all()
#    serializer_class = ExampleSerializer



# Create your views here.
