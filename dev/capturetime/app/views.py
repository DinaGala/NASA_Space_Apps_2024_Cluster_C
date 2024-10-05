from django.shortcuts import render

# Create your views here.

import requests
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from timezonefinder import TimezoneFinder
import geopandas as gpd
from shapely.geometry import Point
import pytz
import os
import geopandas as gpd
from django.conf import settings
from requests.auth import HTTPBasicAuth
from django.views import View
from pyproj import Proj, transform
from datetime import datetime, timedelta


class NextLandsatCaptureView(View):
    def post(self, request):
        # Get the latitude and longitude from the request body
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        # Convert coordinates to Path and Row
        path, row = self.get_wrs2_path_row(latitude, longitude)

        # Get the last acquisition date
        last_acquisition_date = self.get_last_acquisition(path, row)

        if last_acquisition_date:
            # Calculate the next acquisition date
            next_acquisition_date = last_acquisition_date + timedelta(days=16)

            # Convert to local timezone
            local_tz = pytz.timezone('America/New_York')  # Change to your local timezone
            next_acquisition_local = next_acquisition_date.astimezone(local_tz)

            # Return the next acquisition date
            return JsonResponse({
                'next_acquisition': next_acquisition_local.strftime('%Y-%m-%d %H:%M:%S'),
                'path': path,
                'row': row,
            })
        else:
            return JsonResponse({'error': 'No acquisition data found'}, status=404)

    def get_wrs2_path_row(self, latitude, longitude):
        """Convert latitude and longitude to WRS-2 Path and Row."""
        # This function needs the appropriate logic to determine path and row.
        # You can use the following constants for Landsat 8 and 9:
        wrs2_path_row_data = [
            # Fill with WRS-2 path/row data or use an existing library
            # Example: (path, row, min_latitude, max_latitude, min_longitude, max_longitude)
            (23, 32, 38.0, 40.0, -76.0, -74.0),  # Example values
            # Add more path/row definitions as needed
        ]

        for path_row in wrs2_path_row_data:
            if (latitude >= path_row[2] and latitude <= path_row[3] and
                    longitude >= path_row[4] and longitude <= path_row[5]):
                return path_row[0], path_row[1]

        raise ValueError("Path and Row not found for the given coordinates")

    def get_last_acquisition(self, path, row):
        """Fetch the last acquisition date for the given Path and Row."""
        # This is a mock function. Replace with actual logic to fetch last acquisition date.
        # You can check against available datasets, either from an API or a local dataset.
        # Here, you could query a CSV or a database that has the historical records.
        
        # For the sake of this example, return a hardcoded date for testing.
        return datetime(2024, 10, 1, 15, 0, 0, tzinfo=pytz.UTC)