# For Python 3.6
#
# This script downloads USGS streamflow data for the CAMELS gauges
# it requires a comma-separated text file with header line where the first column contains the IDs of the USGS stations
# (e.g. point to "camels_attributes_v2.0\camels_topo.txt"
#
# The script uses the USGS automated retrieval option
# https://help.waterdata.usgs.gov/faq/automated-retrievals#DV
#
# Therefore, an URL needs to be generated. Example:
# "https://waterservices.usgs.gov/nwis/dv/?format=rdb&sites=01646500&period=P10400W&siteType=ST&siteStatus=all&parameterCd=00060"
#
# format=rdb - tab delimited text file
# sites=01646500 - site id to be downloaded
# period=P10400W - download all data 10400 weeks from present day (200 years)
# siteType=ST - site type is stream
# siteStatus=all - all status (active and passive)
# parameterCd=00060 - streamflow in ft3 s-1
#
# Station IDs are automatically pasted in line 51 (url = str("https://) below.
# In case other values need to be adjusted, change parameters in line 51 directly
#
# Written by Jens Kiesel
# kiesel@igb-berlin.de
#
# 20.04.2019

import urllib.request
import os

def GetGaugeIDHUC(CAMELS_streamflow_folder):
    gaugeID_HUC_dic = {}
    HUC_folder_names = os.listdir(CAMELS_streamflow_folder)
    for HUC_folder in HUC_folder_names:
        HUC_folder_path = os.path.join(CAMELS_streamflow_folder, HUC_folder)
        CAMELS_flow_files = os.listdir(HUC_folder_path)
        for CAMELS_flow_file in CAMELS_flow_files:
            gaugeID = str(CAMELS_flow_file.split('_')[0])
            gaugeID_HUC_dic[gaugeID] = HUC_folder
    return gaugeID_HUC_dic


#retrieve stations to download to list
gauge_file = r"c:\CommonData\CAMELS\camels_attributes_v2.0\camels_topo.txt"
CAMELS_streamflow_folder = r"c:\CommonData\CAMELS\basin_dataset_public_v1p2\usgs_streamflow"

out_folder = r"c:\CommonData\USGSStreamflow\From_CAMELS_streamflow_data" #all flow files will be saved
log_file = os.path.join(out_folder,"#log.txt")
gauge_list_from_CAMELS_streamflow_fol = True

if gauge_list_from_CAMELS_streamflow_fol == True:
    gauge_ids = GetGaugeIDHUC(CAMELS_streamflow_folder).keys()
else:
    gauge_ids = []
    with open(gauge_file, 'r') as infile:
        next(infile)
        for line in infile:
            try:
                gauge_id_int = int(line.split(';')[0])
                gauge_ids.append(line.split(';')[0])
            except ValueError:
                print("\nLine: '"+line.replace("\n","")+str("' does not contain valid gauge ID!"))
print(str(len(gauge_ids))+" Station IDs are available\n")

# iterate over gauge IDs and construct download string:
gauge_ids_error = []
for gauge_id in gauge_ids:
    print("Downloading gauge ID: "+gauge_id)
    url = str("https://waterservices.usgs.gov/nwis/dv/?format=rdb&sites="+gauge_id+"&period=P10400W&siteType=ST&siteStatus=all&parameterCd=00060")
    gauge_file = os.path.join(out_folder,gauge_id+".txt")
    try:
        # Download the file from `url`, check if sites were found and if yes, save it locally :
        with urllib.request.urlopen(url) as response:
            data = response.read()  # a `bytes` object
            if data.decode('ascii').startswith("#  No sites found"):
                gauge_ids_error.append(gauge_id)
            else:
                with open(gauge_file, 'wb') as out:
                    out.write(data)
    except:
        gauge_ids_error.append(gauge_id)

# write log file
with open(log_file, 'w') as out:
    if len(gauge_ids_error) > 0:
        print("\nErrors while downloading! Check file : "+str(log_file))
        out.write("The following gauge IDs could not be downloaded or found:\n")
        out.write("\n".join(gauge_ids_error))
    else:
        print("\nDONE")
        out.write(str(len(gauge_ids))+" gauge IDs downloaded")


