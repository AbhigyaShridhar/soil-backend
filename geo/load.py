from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .geo import soilType

dsmw_mapping = {
    'snum': 'SNUM',
    'faosoil': 'FAOSOIL',
    'domsoi': 'DOMSOI',
    'phase1': 'PHASE1',
    'phase2': 'PHASE2',
    'misclu1': 'MISCLU1',
    'misclu2': 'MISCLU2',
    'permafrost': 'PERMAFROST',
    'cntcode': 'CNTCODE',
    'cntname': 'CNTNAME',
    'sqkm': 'SQKM',
    'country': 'COUNTRY',
    'geom': 'MULTIPOLYGON',
}

soil_shp = Path.cwd() / 'DSMW' / 'DSMW.shp'

def run(verbose=True):
    lm = LayerMapping(soilType, soil_shp, dsmw_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
