""" Mask an xarray dataarray or dataset with a polygon in a shapefile.

I have copied this script from https://gist.github.com/bradyrx/1a15d8c45eac126e78d84af3f123ffdb
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import xarray as xr
import numpy as np
from shapely.geometry import Point, Polygon
from pathlib import Path


def select_shape(shpfile, category, name, plot=True):
    """Select the submask of interest from the shapefile.
    Args:
        shpfile: (*.shp) loaded through `load_shape_file`
        category: (str) header of shape file from which to filter shape.
            (Run print(shpfile) to see options)
        name: (str) name of shape relative to category.
        plot: (optional bool) if True, plot the polygon that will be masking.
    Returns:
        shapely polygon
    Example:
        from esmask.mask import load_shape_file, select_shape
        LME = load_shape_file('LMEs.shp')
        CalCS = select_shape(LME, 'LME_NAME', 'California Current')
    """
    s = shpfile
    polygon = s[s[category] == name]
    polygon = polygon.geometry[:].unary_union

    if plot:
        f, ax = plt.subplots()
        ax.add_patch(PolygonPatch(polygon, fc='#6699cc', ec='#6699cc',
                     alpha=0.5))
        ax.axis('scaled')
        plt.show()
    return polygon

def serial_mask(lon, lat, polygon):
    """Masks longitude and latitude by the input shapefile.
    Args:
        lon, lat: longitude and latitude grids.
            (use np.meshgrid if they start as 1D grids)
        polygon: output from `select_shape`. a shapely polygon of the region
                 you want to mask.
    Returns:
        mask: boolean mask with same dimensions as input grids.
    Resource:
       adapted from https://stackoverflow.com/questions/47781496/
                    python-using-polygons-to-create-a-mask-on-a-given-2d-grid
    """
    # You might need to change this...
    if ((len(lon.shape) != 2) | (len(lat.shape) != 2)):
        raise ValueError("""Please input a longitude and latitude *grid*.
            I.e., it should be of two dimensions.""")
    lon, lat = np.asarray(lon), np.asarray(lat)
    # convert to -180 to 180, as I expect most shapefiles are that way.
    lon[lon > 180] = lon[lon > 180] - 360
    lon1d, lat1d = lon.reshape(-1), lat.reshape(-1)
    # create list of all points in longitude and latitude.
    a = np.array([Point(x, y) for x, y in zip(lon1d, lat1d)], dtype=object)
    # loop through and check whether each point is inside polygon.
    mask = np.array([polygon.contains(point) for point in a])
    # reshape to input grid.
    mask = mask.reshape(lon.shape)
    return mask

#%%
shp = gpd.read_file(r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis\vg2500_geo84\vg2500_bld.shp")
thuringia = select_shape(shp, 'GEN', 'Thueringen', plot=True)
da = xr.open_dataset(Path(r'C:\Users\sb123\Documents\OneDrive\04_SS22'
                          r'\climThesis\pr_hyras_1_2020_v5-0_de.nc'))['pr']
mask = serial_mask(da.lon, da.lat, thuringia)
# mask = xr.DataArray(mask, dims=['lat', 'lon']) # dims should be like your base data array you'll be maski
# da2 = da.where(mask)
# fig, ax = plt.subplots()
# da[0,:,:].plot(ax=ax)
# fig.show()