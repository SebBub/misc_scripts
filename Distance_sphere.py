"""Calculate the horizontal distance on a sphere from POI (lat0, lon0)
to all other gridpoints on the sphere"""

import numpy as np
r_e = 6.371e6    #Earth radius

# usually -90:90 and -180:180 for Earth, in this case just Atlantic ocean
lat = np.arange(-59.5, 61.5, 1) #deg
lon = np.arange(-59.5, 1.5, 1)  #deg

longitude, latitude = np.meshgrid(lon,lat)

def dist_on_sphere(lat_0, lon_0, lat, lon): #https://en.wikipedia.org/wiki/Great-circle_distance
    return r_e * (
        np.arccos(np.sin(lat_0 * np.pi / 180.) * np.sin(lat * np.pi / 180.) +
                  np.cos(lat_0 * np.pi / 180.) * np.cos(lat  * np.pi / 180.)
                  * np.cos((lon_0 - lon) * np.pi / 180.))
    )

dist = dist_on_sphere(lat[-1], lon[0], latitude, longitude) #POI = NW corner
# (deepwater formation in Labrador sea)