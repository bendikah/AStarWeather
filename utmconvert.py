from pyproj import Proj

# Script to convert utm coordinates to lat lon, and vice versa

def utm_to_lat_lon(zone, east, north):
    myProj = Proj("+proj=utm +zone=%s, +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs" % zone)
    lon, lat = myProj(east, north, inverse=True)
    return lon, lat


def lat_lon_to_utm(zone, lon, lat):
    myProj = Proj("+proj=utm +zone=%s, +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs" % zone)
    east, north = myProj(lon, lat, inverse=False)
    return east, north
