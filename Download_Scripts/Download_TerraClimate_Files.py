# DOES NOT WORK ANYMORE
# use wget script and run in Cygwin:
# 0. download eines WGET shell scriptes über terraclimate interface
# 2. kopiere die terraclimate_wget.sh in das CygwinWGET Verzeichnis
# 3. starte cygwin und navigiere mit "cd .." und "cd verzeichnis" in das Unterverzeichnis
# 5. tippe "bash terraclimate_wget.sh"

import os
import shutil
import requests

headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/37.0.2049.0 Safari/537.36'
}

out_folder = r'c:\Temp'

errors = []
pathname = r'http://thredds.northwestknowledge.net:8080/thredds/catalog/TERRACLIMATE_ALL/data/catalog.html?dataset=TERRACLIMATE_ALL_SCAN/data'
for year in range(1980, 2020):
#for year in range(1):
    for tmp in ['tmin', 'tmax']:
        url = os.path.join(pathname, "TerraClimate_"+ str(tmp) + "_" + str(year) + ".nc")
        url = "http://thredds.nhttp://thredds.northwestknowledge.net:8080/thredds/fileServer/TERRACLIMATE_ALL/data/TerraClimate_"+ str(tmp) + "_" + str(year) + ".nc"
        #url = "http://thredds.nhttp://thredds.northwestknowledge.net:8080/thredds/fileServer/TERRACLIMATE_ALL/data/TerraClimate_aet_2016.nc"
        download_file = os.path.join(out_folder, os.path.split(url)[-1])
        print(download_file)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(download_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
print("DONE")