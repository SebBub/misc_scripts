# this script downloads all years of user defined parameters from the princeton website:
# http://hydrology.princeton.edu/data/pgf/v3

import pandas as pd
import os
import urllib.request


out_folder = r'f:\#Storage\princeton_climate'
parameters = ['prcp', 'tmax', 'tmin']
start_yr = 1948
end_yr = 2016
years = [yr for yr in range(start_yr, end_yr, 1)]

errors = []
for parameter in parameters:
    for year in years:
        filename = '%s_daily_%d-%d.nc'%(parameter,year,year)
        url = str("http://hydrology.princeton.edu/data/pgf/v3/0.25deg/daily/"+filename)
        print(url)
        download_file = os.path.join(out_folder,url.split('/')[-1])
        try:
            urllib.request.urlretrieve(url, download_file)
            print("Downloaded: "+str(download_file))
        except:
            errors.append(url)


# write log file
with open(log_file, 'w') as out:
    if len(errors) > 0:
        print("\nErrors while downloading! Check file : "+str(log_file))
        out.write("The following gauge IDs could not be downloaded or found:\n")
        out.write("\n".join(errors))
    else:
        print("\nDONE")
        out.write(str(len(errors))+" gauge IDs downloaded")

print("DONE")