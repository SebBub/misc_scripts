# TODO learn how to create issues and push them to GITHUB
""" Plot grid of .nc files at a specified area.

This script overlays the grids of two .nc files on a map for visualisation
around a point (lat/lon). Main objective  is to quickly get a feeling for
how spatial dimensions (e.g. topography) and grid spacing relate. Can also
be used to see how many gridpoints fall within the area of interest."""

# Imports
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import xarray as xr
import string
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.ticker as mticker
# set various parameters for the plots, adjust based on your Word document
# formatting
parameters = {"axes.titlesize": 11, "font.family": "Calibri", "font.size": 11,
              "axes.titleweight": "regular", "legend.fontsize": 11,
              "axes.labelsize": 11}
plt.rcParams.update(parameters)
del parameters

# this defines where the map backgrounds reside
os.environ["CARTOPY_USER_BACKGROUNDS"] = str(Path(os.getcwd()) /
                                             "Map_Background")
alphabet = list(string.ascii_lowercase)  # string of all lowercase characters
# point around which grids shall be visualised +- lat/lon - offset
latitude = 51;
longitude = 11  # Erfurt

savefigs_to = Path(r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis"
                   r"\Figures")

# Paths to netCDF files for which grids shall be visualised
datafiles = [r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis\Data"
             r"\Observations\ERA5\ERA5.nc"]

data_arrays = []  # fill empty list during following loop
for datafile in datafiles:
    data_arrays.append(xr.open_dataset(datafile))

grids = []  # fill empty list during following loop
for data_array in data_arrays:  # fill list with lists of coordinates
    try:  # dimension names "latitude" and "longitude"
        grids.append([np.round(data_array.latitude.values, 2), np.round(
            data_array.longitude.values, 2)])
    except:  # dimension names "lat" and "lon"
        grids.append([np.round(data_array.lat.values, 2), np.round(
            data_array.lon.values, 2)])
number_grids = len(grids)  # how many grids to visualise? equals len(datafiles)


# %% Plotting
def plot_grids(overlay=False, offset=5, figsize=(7, 7), shapefile=None):
    if len(grids) == 1:
        overlay = True
    if len(grids) == 0:
        print("Error! Grid list is empty!")

    gridcolors = ["k", "r", "b", "g"]  # extend if needed to overlay more grids

    offset = [longitude - offset, longitude + offset, latitude - offset,
              latitude + offset]
    if shapefile == None:
        states_provinces = cfeature.NaturalEarthFeature(category="cultural",
                                                        name="admin_1_states_provinces",
                                                        scale="50m",
                                                            edgecolor="red")
    else:
        reader = shpreader.Reader(shapefile)
        THU = [entry for entry in reader.records() if entry.attributes[
            "GEN"] == "Thueringen"][0]
        shape_feature = cfeature.ShapelyFeature([THU.geometry],
                                                ccrs.PlateCarree(),
                                       facecolor=None, edgecolor='black',
                                       lw=1)
    if not overlay:
        fig, ax = plt.subplots(ncols=number_grids, figsize=figsize,
                               subplot_kw={"projection": ccrs.PlateCarree()})
        fig.subplots_adjust(left=.05, right=.95, bottom=.2, top=.9, wspace=0.1,
                            hspace=.2)

        for i, grid in enumerate(grids):
            # TODO add plot of topography later
            gl = ax[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                                 linewidth=1, color=gridcolors[i], alpha=0.5,
                                 linestyle="-")
            gl.xlocator = mticker.FixedLocator(grid[1])
            gl.ylocator = mticker.FixedLocator(grid[0])
            ax[i].set_extent(offset, ccrs.PlateCarree())
            ax[i].add_feature(cfeature.BORDERS, linestyle="-")
            ax[i].coastlines(resolution="50m")
            if shapefile is None:
                ax[i].add_feature(states_provinces, edgecolor="gray")
            else:
                ax[i].add_feature(shape_feature)
            ax[i].scatter(longitude, latitude, s=50, marker="x", color="r",
                          label='Erfurt')
            ax[i].annotate(alphabet[i], (0, -.08), xycoords="axes fraction",
                           weight="bold")

    else:
        fig, ax = plt.subplots(figsize=figsize,
                               subplot_kw={"projection": ccrs.PlateCarree()})
        fig.subplots_adjust(left=.05, right=.95, bottom=.2, top=.9, wspace=0.1,
                            hspace=.2)

        for i, grid in enumerate(grids):
            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                              linewidth=1, color=gridcolors[i], alpha=0.5,
                              linestyle="-")
            gl.xlocator = mticker.FixedLocator(grid[1])
            gl.ylocator = mticker.FixedLocator(grid[0])
            ax.set_extent(offset)
            ax.coastlines(resolution="50m")
            if shapefile is None:
                ax.add_feature(states_provinces, linestyle="-")
            else:
                ax.add_feature(shape_feature)
            ax.scatter(longitude, latitude, s=50, marker="x", color="r",
                       label='Erfurt')
            ax.legend()

    fig.show()
    # fig.savefig(savefigs_to / "ERA5.png",
    #             dpi=500)


if __name__ == "__main__":
    shape = r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis\Data\Geo" \
            r"\vg250_12-31.utm32s.shape.ebenen\vg250_12-31.utm32s.shape" \
            r".ebenen\vg250_ebenen_1231\VG250_LAN.shp"
    plot_grids(overlay=True, shapefile=shape)
