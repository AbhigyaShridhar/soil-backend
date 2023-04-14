from django.contrib.gis.db import models

# Create your models here.
class soilType(models.Model):
    snum = models.IntegerField()
    faosoil = models.CharField(max_length=17, verbose_name='Texture')
    domsoi = models.CharField(max_length=8, verbose_name='Dominant soil')
    phase1 = models.CharField(max_length=8, null=True, verbose_name='Sub phase1')
    phase2 = models.CharField(max_length=8, null=True, verbose_name='Sub phase2')
    misclu1 = models.CharField(max_length=9, null=True, verbose_name='Land type phase1')
    misclu2 = models.CharField(max_length=9, null=True, verbose_name='Land type phase2')
    permafrost = models.CharField(max_length=14, null=True)
    cntcode = models.BigIntegerField()
    cntname = models.CharField(max_length=10)
    sqkm = models.FloatField()
    country = models.CharField(max_length=50)

    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = 'dsmw'
