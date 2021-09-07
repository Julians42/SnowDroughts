# basic packages
from dask.base import compute
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec # custom layouts
from matplotlib import cm
import pandas as pd
from glob import glob
import time

# packages for netcdfs
import xarray as xr
import dask
import bottleneck
import datetime as dt
from netCDF4 import Dataset, date2num
import cftime

# packages for shape files and masking netcdfs
from shapely import wkb, wkt
from shapely.geometry import Point, shape, Polygon, MultiPolygon
from descartes import PolygonPatch
from matplotlib.collections import PatchCollection
from rasterio import features
import geopandas as gpd
import regionmask # for selecting regions from xarray

from scipy.stats import norm
from statsmodels.distributions.empirical_distribution import ECDF


# load shapefile data from geopandas
gpd_HUC2 = gpd.read_file("/nbhome/Julian.Schmitt/shape/huc2_regions.shp")
gpd_HUC4 = gpd.read_file("/nbhome/Julian.Schmitt/shape/huc4_regions.shp")

# load regions into Polygon objects
HUC2 = [poly.buffer(0) for poly in gpd_HUC2['geometry']]
HUC4 = [poly.buffer(0) for poly in gpd_HUC4['geometry']]

# create HUC2 mask and add to dataset
HUC2_names, HUC2_abbrev = gpd_HUC2['Name'], gpd_HUC2['HUC2']
RM2 = regionmask.Regions(HUC2, names = HUC2_names.values, abbrevs=HUC2_abbrev.values)

# create HUC4 mask
HUC4_names, HUC4_abbrev = gpd_HUC4['Name'], gpd_HUC4['HUC4']
RM4 = regionmask.Regions(HUC4, names = HUC4_names.values, abbrevs=HUC4_abbrev.values)

lat_new = np.arange(25, 53, 0.5) # 1/2 degree grid for comparison with livneh
lon_new = np.arange(235.5, 293, 0.5)

HUC2_drought = RM2.mask(lon_new, lat_new) # create mask over dataset lat-lon
HUC4_drought = RM4.mask(lon_new, lat_new) # create mask over dataset lat-lon

# get filenames
ensemble_members = glob("/decp/SPEAR_MED/SPEAR_c192_o1_Hist_AllForc_IC1921_K50/"
                        "pp_ens_*/atmos/ts/monthly/94yr/atmos.192101-201412.precip.nc")


def compute_SWEI(dataset, month):
    ds = dataset.sel(time=dataset['time.month']==month)
    return xr_to_SWEI(ds)

def compute_member_swei(spear_file):
    """Computes and saves SWEI by HUC2 region for SPEAR ensemble member"""
    start_time = time.time()
    # load file, add HUC2 mask, and groupby region
    spear_hist = mask_ensemble(process_ensemble(spear_file))
    
    # do swei computation by month (simpler to code, but slower computationally)
    #monthly_swei = Parallel(n_jobs=13)(delayed(compute_SWEI)(spear_hist, month) for month in range(1,13))
    monthly_swei = [compute_SWEI(spear_hist, month) for month in range(1,13)]
    
    # combine files and save
    index = spear_file.split("/")[4].split("_")[-1] # ensemble member number
    ensemble_xr = xr.concat(monthly_swei, dim='time').sortby('time')
    
    # summarize
    execution_time = time.time() - start_time
    print(f"Computed SWEI for ensemble member {index} in {execution_time} seconds.")
    return ensemble_xr, index
    
def to_swei(ar):
    """Takes numpy array of swe values and returns SWEI values"""
    SWEI = norm.ppf(ECDF(ar, side='right')(ar))
    SWEI = np.where(SWEI==np.inf, -np.min(SWEI), SWEI) # care less about max W4 - replace symmetrically
    return SWEI

def xr_to_SWEI(ds):
    # grab data to numpy
    ar = []
    try:
        ar = np.array(ds.precip)
    except:
        ar = np.array(ds.precip)
        
    # convert to SWEI
    SWEI_data = np.array(list(map(lambda x: to_swei(x), ar)))
    
    # convert back to dataarray and return new ds
    ds_swei = ds.copy()
    try:
        ds_swei.precip.data = xr.DataArray(SWEI_data)
    except:
        ds_swei.precip.data = xr.DataArray(SWEI_data)
    return ds_swei

def process_ensemble(file):
    """Processses ensemble file to match livneh dataset. Returns April"""
    hist = xr.open_dataset(file).load()
    lat_new = np.arange(25, 53, 0.5) # 1/2 degree grid for comparison with livneh
    lon_new = np.arange(235.5, 293, 0.5)
    hist = hist.sel(time=slice("1921", "2011")).resample(time="1M").mean().reindex(lat=lat_new, 
                                                        lon=lon_new, method='nearest')
    #hist = hist.sel(time=hist['time.month']==4)
    return hist
    
def mask_ensemble(hist):
    ds_HUC2 = hist.copy()
    ds_HUC2['mask'] = HUC2_drought
    
    ds_HUC2 = ds_HUC2.groupby('mask').mean()
    ds_HUC2 = ds_HUC2.assign_coords(regions=("mask", RM2.names))
    return ds_HUC2

def save_hist_nc(hist_ens, index):
    try: ncfile.close()  # just to be safe, make sure dataset is not already open.
    except: pass
    ncfile             = Dataset(f'/work/Julian.Schmitt/data/precipi/monthly_ens_{index}.nc',mode='w',format='NETCDF4') 
    # create dimension 
    mask_dim           = ncfile.createDimension('mask', 18)     
    time_dim           = ncfile.createDimension('time', 1092)    
    for dim in ncfile.dimensions.items():
        print(dim)
    # generate header
    ncfile.title       ='PRECIP Index from SPEAR'
    # define variables 
    mask               = ncfile.createVariable('mask', np.float32, ('mask',))
    mask.units         = 'none'
    mask.long_name     = 'mask'
    time               = ncfile.createVariable('time', np.float32, ('time',))
    time.units         = 'days since 1921-01-01'
    time.long_name     = 'time'
    precip               = ncfile.createVariable('precip', np.float64,('mask','time')) # note: unlimited dimension is leftmost
    precip.units         = 'none' 
    precip.standard_name = 'PRECIP_I z-score'  
    print(precip)
    # write data into matrix
    mask[:]   = np.array(hist_ens.mask)
    time[:]   = date2num(hist_ens.time,'days since 1921-01-01')
    precip[:,:] = np.squeeze(np.array(hist_ens.precip))
    #save data and close the file
    ncfile.close(); print('Dataset is closed!')

for file in ensemble_members:
    # compute
    hist_ens, index = compute_member_swei(file)
    # save file
    save_hist_nc(hist_ens, index)