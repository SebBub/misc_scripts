# this script constructs all possible time series for the MODIS NRT Flood Waters Product from NASA
# and tries to download the files
# it downloads the 3-day composites (those date back in time longest)
# please check here for additional products (copy link from download)
# https://floodmap.modaps.eosdis.nasa.gov/getTile.php?location=100E020N&day=234&year=2005&product=3

import pandas as pd
import os
import urllib.request


# ONLY DOWNLOAD THE NEWEST ONES - DO NOT OVERWRITE EXISTING BECAUSE THEY ARE CLIPPED TO THE SMALLEST EXTENT

lat = "020N" #"010N"
lon = "100E"
start_date = "2003-12-31"  # data starts in 2003
end_date = "2018-12-31"
product = "MSW"  # modis surface water  "MWP"  # modis water product
if product == "MSW":
    folder = "SurfaceWater"
elif product == "MWP":
    folder = "WaterProduct"
out_folder = os.path.join(r'c:\Users\jensk\Work\01_Projects\190423hlo_MRC_AMFR2017_2018\02_Data\MODIS_Floodmaps\A14x3D3OT_0noWater_1Water', folder, lon+lat)

all_dates = pd.date_range(start=start_date, end=end_date)

errors = []
for date in all_dates:
    year = str(date.year)
    doy = '%03d'%(date.dayofyear)
    url = str("https://floodmap.modaps.eosdis.nasa.gov/Products/"+lon+lat+"/"+year+"/"+product+"_"+year+doy+"_"+lon+lat+"_3D3OT.tif")
    print(url)
    download_file = os.path.join(out_folder,url.split('/')[-1])
    try:
        urllib.request.urlretrieve(url, download_file)
        print("Downloaded: "+str(download_file))
    except:
        errors.append(url)

"""
# write log file
with open(log_file, 'w') as out:
    if len(errors) > 0:
        print("\nErrors while downloading! Check file : "+str(log_file))
        out.write("The following gauge IDs could not be downloaded or found:\n")
        out.write("\n".join(errors))
    else:
        print("\nDONE")
        out.write(str(len(errors))+" gauge IDs downloaded")
"""
print("DONE")