""" Simple script to plot a gridded file to a map.

Relies on `xarray`, `matplotlib` and `cartopy` libraries.
"""
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
from pathlib import Path


def plot_grid(dataset_path, var=None):
    """
    This function takes a path to a data array and plots the first timestep
    on a map.
    Parameters
    ----------
    dataarray : str
        `dataarray` is a raw string to the path of the dataset
    var : str
        `var` is the name of the variable in the dataset which shall be plotted
    Returns
    -------
    """
    if var is None:
        da = xr.open_dataarray(dataset_path)
    else:
        da = xr.open_dataset(dataset_path)[var]
    fig, ax = plt.subplots()
    da.plot(ax=ax)
    plt.tight_layout()
    fig.show()


if __name__ == '__main__':
    # plot_grid(r'C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis'
    #           r'\pr_hyras_1_2020_v5-0_de.nc', 'pr')

    # plot_grid(r'C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis\2016.nc',
    #           'pr')

    plot_grid(r"C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis"
              r"\clim_pr_hyras_1_2012_v5-0_de.nc")
