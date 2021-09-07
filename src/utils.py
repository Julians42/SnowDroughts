from imports import *
# Functions for Computing SWEI indicies
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
        ar = np.array(ds.snow)
    except:
        ar = np.array(ds.swe)
        
    # convert to SWEI
    SWEI_data = np.array(list(map(lambda x: to_swei(x), ar)))
    
    # convert back to dataarray and return new ds
    ds_swei = ds.copy()
    try:
        ds_swei.snow.data = xr.DataArray(SWEI_data)
    except:
        ds_swei.swe.data = xr.DataArray(SWEI_data)
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
    ncfile             = Dataset(f'/work/Julian.Schmitt/data/swei/monthly_ens_{index}.nc',mode='w',format='NETCDF4') 
    # create dimension 
    mask_dim           = ncfile.createDimension('mask', 18)     
    time_dim           = ncfile.createDimension('time', 1092)    
    for dim in ncfile.dimensions.items():
        print(dim)
    # generate header
    ncfile.title       ='SWEI from SPEAR'
    # define variables 
    mask               = ncfile.createVariable('mask', np.float32, ('mask',))
    mask.units         = 'none'
    mask.long_name     = 'mask'
    time               = ncfile.createVariable('time', np.float32, ('time',))
    time.units         = 'days since 1921-01-01'
    time.long_name     = 'time'
    snow               = ncfile.createVariable('snow', np.float64,('mask','time')) # note: unlimited dimension is leftmost
    snow.units         = 'none' 
    snow.standard_name = 'SWEI z-score'  
    print(snow)
    # write data into matrix
    mask[:]   = np.array(hist_ens.mask)
    time[:]   = date2num(hist_ens.time,'days since 1921-01-01')
    snow[:,:] = np.squeeze(np.array(hist_ens.snow))
    #save data and close the file
    ncfile.close(); print('Dataset is closed!')
