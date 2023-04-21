#from django.contrib.gis.geoip2 import GeoIP2
from django.http import JsonResponse
from .models import soilType
import pandas as pd
import geocoder
from django.contrib.gis.db.models.functions import Transform
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.db.models.functions import Area
from django.contrib.gis.db.models.functions import Intersection
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

def getData():
    xls = pd.ExcelFile('Crop_Recommendation_Dataset.xlsx')
    data = pd.read_excel(xls, 'Sheet1')
    res = {}
    for code in data['Code'].unique():
        subset = data[data['Code'] == code]
        soil_type = subset.iloc[0]['Soil Type']
        subtype = subset.iloc[0]['Subtype']
        recommendations = subset.iloc[0]['Recommendations']
        res[code] = {'Soil Type': soil_type, 'Subtype': subtype, 'Recommendations': recommendations}
    return res


@csrf_exempt
@staff_member_required(login_url='/admin/login/')
@login_required
def get_soil_detail(request):
    # Get the latitude and longitude of the clicked point
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    point = Point(float(lng), float(lat), srid=4326)

    # Find the nearest soilDetail object to the clicked point
    soil_detail = soilType.objects.filter(geom__distance_lte=(point, D(m=5000))) \
        .annotate(distance=Distance('geom', point)) \
        .order_by('distance') \
        .first()

    # Render a JSON response with the soilDetail data

    dataSet = getData()
    res = dataSet[soil_detail.domsoi]
    soil_t = res['Soil Type']
    subtype = res['Subtype']
    recommendations = res['Recommendations']
    description = {'Soil Type': soil_t, 'Subtype': subtype, 'Recommendations': recommendations}

    return JsonResponse({
        'id': soil_detail.id,
        'name': soil_detail.domsoi,
        'description': description,
        'geom': soil_detail.geom.json,
    })


def get_user_location_mapping(request):
    """x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    g = GeoIP2()"""
    g = geocoder.ip("me")
    lon, lat = g.latlng[0], g.latlng[1]
    pnt = Point(lat, lon)
    location = soilType.objects.get(geom__intersects=pnt)
    domsoi = location.domsoi
    dataSet = getData()
    res = dataSet[domsoi]
    return JsonResponse({
        'soil_type': res['Soil Type'], 'subtype': res['Subtype'], 'recommendations': res['Recommendations'], 'id': location.id
    })
