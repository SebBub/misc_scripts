#%%
# the script is based on Jens' script for MODIS data
# the crawler is built to auto download many csv files for GSOD station observations
# Dataset: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00861
# https://www.ncei.noaa.gov/access/search/data-search/global-hourly?bbox=-9.395,147.144,-9.515,147.264

import pandas as pd
import os
import urllib.request
from datetime import date

# ONLY DOWNLOAD THE NEWEST ONES - DO NOT OVERWRITE EXISTING BECAUSE THEY ARE CLIPPED TO THE SMALLEST EXTENT
# Link example https://www.ncei.noaa.gov/data/global-hourly/access/2002/92035099999.csv
# https://www.ncei.noaa.gov/data/global-hourly/access/1950/94035099999.csv
out_folder = '/Volumes/4TB_Lacie/00CLIMATE_DATA/GSOD/'
#  MOMOTE MANUS ISLAND, PP (94044099999.csv)
#  PORT MORESBY JACKSONS INTERNATIONAL, PP (92035099999.csv)
# DARU W.O., PP (94003099999.csv)

station_id = ['94044099999', '94003099999', '92035099999']

#TODO: build loop for all station IDs
#TODO: build section that checks if the file already exists on the local disk
#TODO: use pathlib and understand module...
start_year = 1901
end_year = int(str(date.today())[0:4]) #get current year
all_years = range(start_year, end_year+1)
errors = []

for year in all_years:
    print(str(year))
    url = str("https://www.ncei.noaa.gov/data/global-hourly/access/"+str(year)+"/"+station_id+".csv")
    download_file = os.path.join(out_folder, str(year)+'_'+url.split('/')[-1]) # split() method splits string into list separated by separator
    print("Trying to download: "+url+" to " + download_file)
    try:
        urllib.request.urlretrieve(url, download_file)
        print("Downloaded: " + str(download_file)+'!\n')
    except:
        errors.append(url)
        print("That didnt work!\n")

print("DONE")

#%%

"""
# # write log file
# with open(log_file, 'w') as out:
#     if len(errors) > 0:
#         print("\nErrors while downloading! Check file : "+str(log_file))
#         out.write("The following gauge IDs could not be downloaded or found:\n")
#         out.write("\n".join(errors))
#     else:
#         print("\nDONE")
#         out.write(str(len(errors))+" gauge IDs downloaded")
"""
