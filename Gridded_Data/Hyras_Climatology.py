""" This script computes the climatology from DWD Hyras data for the given
spatial domain specified by a shapefile

"""

from pathlib import Path
import xarray as xr
from Mask_Shapefile import *

if __name__ == '__main__':
    # Step 1: Define mask for Thuringia
    shp = gpd.read_file(r"C:\Users\sb123\Documents\OneDrive\04_SS22"
                        r"\climThesis\vg2500_geo84\vg2500_bld.shp")
    thuringia = select_shape(shp, 'GEN', 'Thueringen', plot=False)
    # exemplary dataarray to get the coordinates from
    da = xr.open_dataset(Path(r'C:\Users\sb123\Documents\OneDrive\04_SS22'
                              r'\climThesis\pr_hyras_1_2020_v5-0_de.nc'))['pr']
    mask = serial_mask(da.lon, da.lat, thuringia)

    # Step 2: Read in netCDF files, aggregate over year, then save to netCDF
    datapath = Path(r'C:\Users\sb123\Documents\OneDrive\04_SS22\climThesis')
    # TODO add code for selecting start and endyear and return error when
    # missing data
    files = list(datapath.glob('pr_hyras*.nc'))
    for file in files:
        da = xr.open_dataset(file)['pr']
        da = da.where(mask)
        da = da.sum(dim='time')
        da.to_netcdf(path=datapath / ('clim_' + file.parts[-1]))
