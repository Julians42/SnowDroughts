import os
import numpy as np
import time

import matplotlib.ticker as mticker
import pandas as pd
from glob import glob
import statsmodels as sm
from scipy.stats import norm, gamma
from statsmodels.distributions.empirical_distribution import ECDF

# packages for netcdfs
import xarray as xr
import dask
import bottleneck
import datetime as dt

startTime = time.time()
print(startTime)
# open data
swe = xr.open_mfdataset("/Users/julianschmitt/Downloads/NOAA/climatology/swe_reindexed.nc")
t_low_r = xr.open_mfdataset("/Users/julianschmitt/Downloads/NOAA/climatology/t_low_regridded.nc")
t_high_r = xr.open_mfdataset("/Users/julianschmitt/Downloads/NOAA/climatology/t_high_regridded.nc")
prec_r = xr.open_mfdataset("/Users/julianschmitt/Downloads/NOAA/climatology/prec_regridded.nc")

# focus on swe first
# take 3 month rolling average 
ds2 = swe.resample(time="1M").mean().rolling(time=3).mean()

lat_new = np.arange(32, 49, 0.5)
lon_new = np.arange(235, 255, 0.5)
gp = ds2.reindex(lat=lat_new, lon=lon_new, method='nearest').sel(time=ds2['time.month']==4).stack(z=['lat','lon']).groupby('z')

# get SWEI
trend = gp.map(lambda ar: xr.DataArray(norm.ppf(ECDF(ar.to_array()[0]).y)[np.argsort(np.array(ar.to_array()[0]))]))

trend_unstacked = trend.unstack('z')

# save 
trend_unstacked.to_netcdf("/Users/julianschmitt/Downloads/NOAA/climatology/livneh_SWEI.nc")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))