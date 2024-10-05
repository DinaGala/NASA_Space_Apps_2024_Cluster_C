from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

# API Key от N2YO (зарегистрируйтесь и получите ключ)
API_KEY = '8VBB7W-PHAH5H-2K2JR9-5CIX'

# ID спутника Landsat 8
# NORAD IDs for Landsat 8 and Landsat 9
LANDSAT_8_NORAD_ID = 39084
LANDSAT_9_NORAD_ID = 49260

# Function to convert UTC timestamp to local time
def convert_utc_to_local(utc_time, local_timezone):
    utc_time = datetime.utcfromtimestamp(utc_time)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

# Function to fetch satellite passes
def get_satellite_passes(norad_id, latitude, longitude, altitude):
    url = f'http://api.n2yo.com/rest/v1/satellite/visualpasses/{norad_id}/{latitude}/{longitude}/{altitude}/10/10/&apiKey={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('passes', [])
    else:
        return []

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
    landsat_9_passes = get_satellite_passes(LANDSAT_9_NORAD_ID, latitude, longitude, altitude)
    
    # Extract the start and end times in local time for both satellites
    result = {
        'landsat_8': [],
        'landsat_9': []
    }
    
    for p in landsat_8_passes:
        result['landsat_8'].append({
            'start_time': convert_utc_to_local(p['startUTC'], local_timezone),
            'end_time': convert_utc_to_local(p['endUTC'], local_timezone),
        })
    
    for p in landsat_9_passes:
        result['landsat_9'].append({
            'start_time': convert_utc_to_local(p['startUTC'], local_timezone),
            'end_time': convert_utc_to_local(p['endUTC'], local_timezone),
        })
    
    # Return the times as JSON response
    return JsonResponse(result)