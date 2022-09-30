from imports import * # import basic packages
from utils import * # import helper functions


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
                        "pp_ens_*/land/ts/monthly/94yr/land.192101-201412.snow.nc")




# Process files and save
for file in ensemble_members:
    # compute
    hist_ens, index = compute_member_swei(file)
    # save file
    save_hist_nc(hist_ens, index)
