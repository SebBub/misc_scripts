#TODO add to Gitlab Repo for collaboration with Jens!
#%%
# the script is based on Jens" script for MODIS data
# the crawler is built to auto download many gzip files for GPCC netCDF files
# Dataset: https://opendata.dwd.de/climate_environment/GPCC/full_data_daily_V2018/

import urllib.request
from pathlib import Path
import gzip

# Example link:
# https://opendata.dwd.de/climate_environment/GPCC/full_data_daily_V2018/full_data_daily_v2018_1982.nc.gz

out_folder = Path("H:/00CLIMATE_DATA/GPCC/")

#TODO: build section that checks if the file already exists on the local disk
#TODO: use pathlib and understand module...
start_year = 1982 #check manually
end_year = 2016 #check mannually
all_years = range(start_year, end_year+1)
errors = []

for year in all_years:
    print(str(year))
    url = str("https://opendata.dwd.de/climate_environment/GPCC/full_data_daily_V2018/full_data_daily_v2018_"+str(year)
              +".nc.gz")
    download_file = out_folder / (str(year)+".nc.gz")
    print("Trying to download: "+url+" to " + str(download_file))
    try:
        urllib.request.urlretrieve(url, download_file)
        print("Downloaded: " + str(download_file)+"!\n")
    except:
        errors.append(url)
        print("That didnt work!\n")

print("DONE - check errors_list for errors!")

