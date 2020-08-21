# encoding: utf-8

"""
Here are some additional methods, load_mapdata is useful for drawing maps.
get_shapelist can convert Geopandas`s GeoDataFrame into map data applicable to this package.
dump_mapdata allows users to save the map data themselves.

"""

from os.path import dirname,join
import json

def get_shapelist(shp,shp_name='shp',vessel={}):
    shps = json.loads(shp.geometry.to_json())
    res_shps = []
    for shape in shps['features']:
        shape = shape['geometry']['coordinates']
        if len(shape) == 1:
            if isinstance(shape[0][0],list):
                res_shps.append(shape[0])
        else:
            for i in range(len(shape)):
                if isinstance(shape[i][0][0],list):
                    res_shps.append(shape[i][0])
    vessel[shp_name] = res_shps
    return vessel

def load_mapdata(datafile=None):
    if datafile is None:
        datafile = 'mapdata.json'
    filepath = join(dirname(__file__),'data',datafile)
    with open(filepath,'r') as ob:
        mapdata = json.load(ob)
    return mapdata

def dump_mapdata(obj,filename):
    filepath = join(dirname(__file__),'data','%s.json' % filename)
    with open(filepath,'w') as ob:
        json.dump(obj,ob)
    
