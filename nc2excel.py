# -*- encoding: utf-8 -*-
'''
@File    :   nc2excel.py
@Create  :   2025-05-11 12:38:29
@Author  :   shihx2003
@Version :   1.0
@Contact :   shihx2003@outlook.com
'''

# here put the import lib
import os
import re
import sys
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
import salem

def CalAvgPrec(ds):
    ds = ds.copy()
    precip_value = ds['precip'].values
    times = ds['time'].values
    avg_prec = []
    for i in range(len(times)):
        precip_slice = precip_value[i, :, :]
        mean_prec = np.nanmean(precip_slice)
        avg_prec.append((times[i], mean_prec))
        
    avg_prec_df = pd.DataFrame(avg_prec, columns=['Date', 'avg_prec'])
    avg_prec_df['Date'] = pd.to_datetime(avg_prec_df['Date']) + pd.Timedelta(hours=8)

    return avg_prec_df
events = ['Fuping_20120621', 'Fuping_20120721', 'Fuping_20130628', 
          'Fuping_20130811', 'Fuping_20160718', 'Fuping_20190804', 
          'Fuping_20200717', 'Fuping_20200801', 'Fuping_20200824',]

nc_dif = "F:/Haihe/FinalPaperDate/PSO/best/"
shpfile = "F:/Haihe/FinalPaperDate/PSO/best/阜平流域.shp"
basinshape = gpd.read_file(shpfile)
min_lon, min_lat, max_lon, max_lat = basinshape.total_bounds
print()

saveprec = {}
for event in events:
    basin = event.split('_')[0]
    eventno = event.split('_')[1]
    nc_path = os.path.join(nc_dif, f'{basin}_precip_{eventno}.nc')

    precds = xr.open_dataset(nc_path)
    precds['precip'] = precds['precip_rate'] * 60 * 60
    prec_masked = precds.salem.roi(shape=basinshape).sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))
    prec_masked.to_netcdf(os.path.join(nc_dif, f'{basin}_precip_{eventno}_masked.nc'))
    print(prec_masked)
    avgprec = CalAvgPrec(precds)
    saveprec[eventno] = avgprec

with pd.ExcelWriter(os.path.join(nc_dif, 'precip.xlsx')) as writer:
    for eventno, df in saveprec.items():
        df.to_excel(writer, sheet_name=eventno, index=False)
        print(f"Saved {eventno} to Excel.")

