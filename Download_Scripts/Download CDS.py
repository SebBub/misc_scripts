import cdsapi
from pathlib import Path
import numpy as np
data_folder = Path(r'H:\00CLIMATE_DATA\WGET')
c = cdsapi.Client()
#%%
years = list(np.arange(2016,2020,1).astype('str'))
for year in years:
    c.retrieve(
        'reanalysis-era5-land',
        {
            'format': 'netcdf',
            'area': [
                0, 130, -15,
                155,
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'year': [year,
            ],
            'variable': 'total_precipitation',
        },
        data_folder / ('ERA5_rainfall'+str(year)+'.nc'))
