# basic packages
import os
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
from dask.base import compute
import bottleneck
import datetime as dt
from netCDF4 import Dataset # for saving netcdfs 

# packages for shape files and masking netcdfs
from shapely import wkb, wkt
from shapely.geometry import Point, shape, Polygon, MultiPolygon
#from descartes import PolygonPatch
from matplotlib.collections import PatchCollection
#from rasterio import features
import fiona
#import geopandas as gpd
#import regionmask # for selecting regions from xarray

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature # for plotting HUC2 regions
from cartopy.io.shapereader import Reader

import scipy.stats as st
from scipy.stats import norm, gamma
from statsmodels.distributions.empirical_distribution import ECDF
import random

# for parallel compute
from joblib import Parallel, delayed

# function for selecting winter
def is_winter(month):
    return (month <=4) | (month >=10)