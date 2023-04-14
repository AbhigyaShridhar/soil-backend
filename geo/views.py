#from django.contrib.gis.geoip2 import GeoIP2
from django.http import JsonResponse
from .models import soilType
from django.contrib.gis.geos import Point
import pandas as pd
import geocoder

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
