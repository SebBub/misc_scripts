# TODO import function from unzip that unzips all these downloads and deletes the original archive containers
# TODO add function that automatically merges the desired band combinations (GDAL?) and saves these as separate GeoTiffs

from landsatxplore.api import API #for searching
from landsatxplore.earthexplorer import EarthExplorer #for downloading
import json #for writing the results to disk
from pathlib import Path

outputdir = Path(r'H:\01Satellite_Data\Germany\Sentinel')

# SEARCHING
# Initialize a new API instance and get an access key
api = API('bubi1080', 'EarthScience2017')

# Search for scenes ()
dataset = 'sentinel_2a' #see here for supported datasets: https://github.com/yannforget/landsatxplore
scenes = api.search(
    dataset=dataset,
    latitude=54.82138127,
    longitude=9.65196384,
    start_date='2020-11-01',
    end_date='2021-03-20',
    max_cloud_cover=10
)

print(f"{len(scenes)} scenes found.")

#WRITING RESULTS TO DISK
entity_ids = [0] * len(scenes)
for i,scene in enumerate(scenes):
    print(scene['acquisition_date'].strftime('%Y-%m-%d'))

    if dataset == 'sentinel_2a':
        # write the unique identifiers to a list for download in a loop
        entity_ids[i] = scene['sentinel_entity_id']

        # # Write scene footprints to disk
        # fname = f"{scene['sentinel_entity_id']}.geojson"
        # with open(fname, "w") as f:
        #     json.dump(scene['spatial_coverage'].__geo_interface__, f)

    elif dataset == 'landsat_ot_c2_l2': #Landsat 8 Collection 2 Level 2
        # write the unique identifiers to a list for download in a loop
        entity_ids[i] = scene['landsat_product_id']

        # # write the unique identifiers to a list for download in a loop
        # fname = f"{scene['landsat_product_id']}.geojson"
        # with open(fname, "w") as f:
        #     json.dump(scene['spatial_coverage'].__geo_interface__, f)

# Log out
api.logout()

#%% DOWNLOADING
ee = EarthExplorer('bubi1080', 'EarthScience2017')

files = list(outputdir.glob('*')) #create a list of filenames already in directory
for i,file in enumerate(files): #extract file
    if (file.stat().st_size / (1024**2)) < 50: # ignore only partially loaded files, e.g. initially aborted
        files[i] = file.name
    else:
        continue

for scene in entity_ids:
    if scene in files:
        continue
    else:
        ee.download(scene, output_dir=outputdir, timeout=600)

ee.logout()
