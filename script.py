import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import os
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

flood_5m = gpd.read_file('data_files/5m_flood.shp')
hist_flood = gpd.read_file('data_files/historical_flooding.shp')
boundary = gpd.read_file('data_files/Fermanagh_DCA.shp')
l_erne = gpd.read_file('data_files/l_erne.shp')
buildings = gpd.read_file('data_files/Pointer_Fermanagh.shp')
lc = gpd.read_file('data_files/LCM_Fermanagh.shp')


#fig.savefig('Fermanagh.png', dpi=300, bbox_inches='tight')