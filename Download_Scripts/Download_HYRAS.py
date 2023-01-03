""" Script to download HYRAS data from DWD CDS for selected years only.

You can also download the entire dataset (>11 GB) on
https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de
/precipitation/ in one .nc file. This script shall help to collect smaller
sub-samples if you need smaller chunks due to limited space on disk.
"""

import os
import urllib.request
from pathlib import Path

def download(startyear, endyear, download_folder, hyras_version='v5-0'):
    """

    Parameters
    ----------
    startyear : int
    endyear : int
    download_folder : str
        `download_folder` needs to be obtained in the format when
        rightclicking on a folder in Windows and selecting "Copy as path" -
        important - precede with an "r" to define as raw string
    hyras_version : str
        'hyras_evrsion' can be either 'v3-0' or 'v5-0', refer to documentation
        under https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/hyras_de/precipitation/

    Returns
    -------
    """
    for year in range(startyear,endyear+1):
        url = f'https://opendata.dwd.de/climate_environment/CDC' \
              f'/grids_germany/daily/hyras_de/precipitation' \
              f'/pr_hyras_1_{year}_{hyras_version}_de.nc'
        file = Path(download_folder) / url[-26:]
        print(f'Trying to download \n {url[-26:]} \n to folder \n' \
                f'{download_folder}')
        try:
            urllib.request.urlretrieve(url, file)
            print(f'Downloaded file:\n {file}')
        except:
            print(f'Could not download file:\n {url[-26:]}')


if __name__ == "__main__":
    download(startyear=2010, endyear=2020,
             download_folder=r'C:\Users\sb123\Documents\OneDrive\04_SS22'
                             r'\climThesis')