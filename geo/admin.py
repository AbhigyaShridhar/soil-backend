from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.gis import admin as geo_admin
from .models import soilType
from .views import get_user_location_mapping, get_soil_detail
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.contrib.gis.geos import GEOSGeometry


class GeoAdminSite(admin.AdminSite):
    site_header = "CROPS+"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('location/', self.admin_view(get_user_location_mapping), name='get_user_location_mapping'),
        ]
        return my_urls + urls

geo_admin_site = GeoAdminSite(name='geo_admin_site')

class MapAdminSite(geo_admin.AdminSite):
    site_header = "CROPS+"
    index_template = 'admin/map_view.html'

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        soil_detail_data = []
        data = soilType.objects.filter(country='INDIA')
        for soil_detail in data:
            soil_detail_data.append({
                'id': soil_detail.id,
                'name': soil_detail.domsoi,
                'geom': GEOSGeometry(soil_detail.geom).geojson,
            })
        extra_context['pos'] = [20.5937, 78.9629]
        extra_context['soil_detail_data'] = soil_detail_data
        return super().index(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('soilDetail/', self.admin_view(get_soil_detail), name='get_soil_detail'),
        ]
        return my_urls + urls

map_admin_site = MapAdminSite(name='map_admin_site')

class soilTypeAdmin(admin.ModelAdmin):
    search_fields = ['country']
    readonly_fields = [
        'snum',
        'faosoil',
        'domsoi',
        'phase1',
        'phase2',
        'misclu1',
        'misclu2',
        'permafrost',
        'cntcode',
        'cntname',
        'sqkm',
        'country'
    ]

    def has_add_permission(self, request):
        return False  # disable the add button

class SoilDetailAdmin(geo_admin.OSMGeoAdmin):
    list_display = ('domsoi', 'geom')
    modifiable = False
    map_template = 'map_view.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('get_soil_detail/<str:lat>/<str:lon>/', staff_member_required(self.get_soil_detail), name='get_soil_detail'),
        ]
        return my_urls + urls

    def get_soil_detail(self, request, lat, lon):
        point = Point(float(lon), float(lat), srid=4326)
        soil_detail = soilType.objects.filter(geom__contains=point).first()
        if soil_detail:
            return redirect('/map/geo/soilType/%d/change/' % soil_detail.id)
        else:
            return HttpResponseNotFound('Soil detail not found')

geo_admin_site.register(soilType, soilTypeAdmin)
map_admin_site.register(soilType, SoilDetailAdmin)
