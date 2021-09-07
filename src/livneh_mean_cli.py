# Compute Mean Climatologies for Livneh Dataset
from imports import *



# define high level params - filepathing is job specific
rootdir = "/Users/julianschmitt/Downloads/NOAA/"
variables = ["swe", "prec", "tmax", "tmin"]
lat_new = np.arange(32, 52, 0.5)
lon_new = np.arange(235, 255, 0.5)

def is_winter(month):
    return (month <=4) | (month >=10)

def average_winter_climatology(variable):
    # open dataset with lazy loading
    print(os.path.join(rootdir, f"livneh_{variable}/*.nc"))
    ds = xr.open_mfdataset(os.path.join(rootdir, f"livneh_{variable}/*.nc")).sel(time=slice("1921", "2011"))

    # reindex to WUS grid, resample to monthly timescale
    ds = ds.reindex(lat =lat_new, lon=lon_new, method="nearest").resample(time="1M").mean()

    # get average climatology by taking mean
    ds = ds.sel(time=is_winter(ds['time.month'])).mean('time')

    # save file
    ds.to_netcdf(f"/Users/julianschmitt/Downloads/NOAA/climatology/livneh_{variable}_average_climatology.nc")



# iterate through variables
for var in variables:
    tstart = time.time()
    average_winter_climatology(var)
    elapsed = time.time()-tstart
    print(f"Processed {var} mean climatology in {elapsed} seconds.")