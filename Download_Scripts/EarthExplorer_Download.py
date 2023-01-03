# TODO import function from unzip that unzips all these downloads and deletes the original archive containers
# TODO add function that automatically merges the desired band combinations (GDAL?) and saves these as separate GeoTiffs
from landsatxplore.api import API #for searching
from landsatxplore.earthexplorer import EarthExplorer #for downloading
import json #for writing the results to disk
from pathlib import Path
from datetime import date


# SEARCHING FOR SCENES
#see here for supported datasets: https://github.com/yannforget/landsatxplore
def search(outputdir, central_lat, central_lon, start_date, dataset = 'sentinel_2a',
           end_date=date.today().strftime("%Y-%m-%d"), max_cloud_cover = 10, username = 'bubi1080',
           password = 'EarthScience2017', download_geojson_extent=False):
    # Initialize a new API instance and get an access key
    api = API(username, password)
    scenes = api.search(
        dataset=dataset,
        latitude=central_lat,
        longitude=central_lon,
        start_date=start_date,
        end_date = end_date,
        max_cloud_cover=max_cloud_cover
    )

    print(f"{len(scenes)} scenes found:")

    entity_ids = [0] * len(scenes)
    for i,scene in enumerate(scenes):
        print(scene['acquisition_date'].strftime('%Y-%m-%d'))

        if dataset == 'sentinel_2a':
            entity_ids[i] = scene['sentinel_entity_id']
            if download_geojson_extent == True: # Write scene footprints to disk
                fname = outputdir / f"{scene['sentinel_entity_id']}.geojson"
                with open(fname, "w") as f:
                    json.dump(scene['spatial_coverage'].__geo_interface__, f)
        elif dataset == 'landsat_ot_c2_l2': #Landsat 8 Collection 2 Level 2
            entity_ids[i] = scene['landsat_product_id']
            if download_geojson_extent == True:
                fname = outputdir / f"{scene['landsat_product_id']}.geojson"
                with open(fname, "w") as f:
                    json.dump(scene['spatial_coverage'].__geo_interface__, f)
    api.logout() # Log out
    return entity_ids

#DOWNLOADING
def download(entity_ids, outputdir, username = 'bubi1080', password = 'EarthScience2017', filesize = 50):
    ee = EarthExplorer(username, password)
    files = list(outputdir.glob('*')) #create a list of filenames already in directory
    for i,file in enumerate(files): #extract file
        if (file.stat().st_size / (1024**2)) < filesize: # ignore only partially loaded files, e.g. initially aborted
            # which are smaller than a threshold value
            files[i] = file.name
        else:
            continue

    for scene in entity_ids:
        if scene in files:
            continue
        else:
            ee.download(scene, output_dir=outputdir, timeout=600)

    ee.logout()

if __name__ == "__main__":
    # Lake Rweru:
    outputdir = Path(r'H:\01Satellite_Data\Rwanda\Sentinel-2')
    # entity_ids = search(outputdir, -2.3879848, 30.2595119, "2021-01-01", max_cloud_cover=50)
    entity_ids = ['L1C_T36MTC_A021082_20210320T081506', 'L1C_T36MTC_A021125_20210323T082934',
                  'L1C_T35MRT_A021125_20210323T082934', 'L1C_T35MRT_A021082_20210320T081506']
    download(entity_ids, outputdir)