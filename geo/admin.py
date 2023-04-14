from django.contrib import admin
from .models import soilType
from .views import get_user_location_mapping
from django.urls import path

class GeoAdminSite(admin.AdminSite):
    site_header = "CROPS+"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('location/', self.admin_view(get_user_location_mapping), name='get_user_location_mapping'),
        ]
        return my_urls + urls

geo_admin_site = GeoAdminSite(name='geo_admin_site')

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

geo_admin_site.register(soilType, soilTypeAdmin)
