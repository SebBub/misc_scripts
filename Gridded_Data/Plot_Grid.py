""" Plot grid of .nc file at a specified area.

This script plots the grid of a .nc file on a map for visualisation
around a specified points latitude and longitude with a specified +- offset
in zonal and meridional direction. It's main aim is to quickly get a feeling
for how the spatial dimensions of the area of interest and the grid spacing
relate. Can also be used to see how many gridpoints fall within the area of
interest."""

# Imports
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
# import pandas as pd
import xarray as xr
import string

import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.ticker as mticker

# set various parameters for the plots, adjust based on your Word document
# formatting
parameters = {"axes.titlesize": 11, "font.family": "Calibri", "font.size": 11,
              "axes.titleweight": "regular", "legend.fontsize": 11,
              "axes.labelsize": 11}
plt.rcParams.update(parameters)

# this defines where the map backgrounds reside
os.environ["CARTOPY_USER_BACKGROUNDS"] = str(Path(os.getcwd()) /
                                             "Map_Background")
alphabet = list(string.ascii_lowercase)  # string of all lowercase characters
# point around which grids shall be visualised +- lat/lon - offset
latitude = 51 ; longitude = 11  # Erfurt

savefigs_to = Path(r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis")
data_path = Path(r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis")

# names of netCDF files for which grids shall be visualised
datafiles = ["system_5_seasonal-monthly-single-levels.nc"]

data_arrays = [] # fill empty list during following loop
for datafile in datafiles:
    data_arrays.append(xr.open_dataset(data_path / datafile))

grids = [] # fill empty list during following loop
for data_array in data_arrays:# fill list with lists of coordinates
    try: # dimension names "latitude" and "longitude"
        grids.append([np.round(data_array.latitude.values, 2), np.round(
            data_array.longitude.values, 2)])
    except: # dimension names "lat" and "lon"
        grids.append([np.round(data_array.lat.values, 2), np.round(
            data_array.lon.values, 2)])
number_grids = len(grids) #how many grids to visualise? equals len(datafiles)


# %% Plotting

def plot_grids(overlay=False, offset=4, figsize=(7, 7)):
    gridcolors = ["k", "r", "b", "g"]  # extend if needed to overlay more grids
    if not overlay:
        fig, ax = plt.subplots(ncols=number_grids, figsize=figsize,
                               subplot_kw={"projection": ccrs.PlateCarree()})
        fig.subplots_adjust(left=.05, right=.95, bottom=.2, top=.9, wspace=0.1,
                            hspace=.2)
        # aax = fig.add_axes([0.4, 0.02, 0.2, .11], frame_on=True, xticks=[], yticks=[])

        for i, grid in enumerate(grids):
            # TODO add plot of topography later
            # t_l = topo_large.plot.contourf(ax=ax[i], cmap=cm.terrain,
            #                                add_colorbar=False, levels=100)
            ax[i].set_title("Grid for file " + datafiles[i])
            gl = ax[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                                 linewidth=1, color="orange", alpha=0.5,
                                 linestyle="-")
            gl.xlocator = mticker.FixedLocator(grid[1])
            gl.ylocator = mticker.FixedLocator(grid[0])
            ax[i].set_extent(
                [longitude - offset, longitude + offset, latitude - offset,
                 latitude + offset], ccrs.PlateCarree())
            # ax[i]stock_img() # optional, better for larger offsets
            # TODO add tick labels
            ax[i].add_feature(cfeature.BORDERS, linestyle="-")
            ax[i].coastlines(
                resolution="10m")  # these we do not need in Thuringia
            # states_provinces = cfeature.NaturalEarthFeature(
            #     category="cultural",
            #     name="admin_1_states_provinces_lines",
            #     scale="50m",
            #     facecolor="none")
            # ax[i].add_feature(states_provinces, edgecolor="gray")
            ax[i].scatter(longitude, latitude, s=50, marker="x", color="r")
            # TODO see above
            # ax[i].scatter(gridpoints[i, 1], gridpoints[i, 0], s=50, marker="x",
            #               color="orange")
            ax[i].annotate(alphabet[i], (0, -.08), xycoords="axes fraction",
                           weight="bold")
    else:
        fig, ax = plt.subplots(figsize=figsize,
                               subplot_kw={"projection": ccrs.PlateCarree()})
        fig.subplots_adjust(left=.05, right=.95, bottom=.2, top=.9, wspace=0.1,
                            hspace=.2)

        for i, grid in enumerate(grids):
            ax.set_title("Grids for files in " + str(datafiles))
            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                              linewidth=1, color=gridcolors[i], alpha=0.5,
                              linestyle="-")
            gl.xlocator = mticker.FixedLocator(grid[1])
            gl.ylocator = mticker.FixedLocator(grid[0])
            ax.set_extent(
                [longitude - offset, longitude + offset, latitude - offset,
                 latitude + offset], ccrs.PlateCarree())
            # ax[i].stock_img() # optional, better for larger offsets
            # TODO add tick labels
            ax.add_feature(cfeature.BORDERS, linestyle="-")
            ax.coastlines(
                resolution="10m")  # these we do not need in Thuringia
            ax.scatter(longitude, latitude, s=50, marker="x", color="r")

    fig.show()
    fig.savefig(savefigs_to / "ERA5Orig_ERA5CoarseConservativeCDO.png",
                dpi=500)


if __name__ == "__main__":
    plot_grids(overlay=True)
