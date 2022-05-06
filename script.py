import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import os
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

desired_width=320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns',40) # this tells PyCharm to show you the whole head of a table, not just 5 columns


flood_5m = gpd.read_file('data_files/flood_5m.shp')
hist_flood = gpd.read_file('data_files/historical_flooding.shp')
boundary = gpd.read_file('data_files/Fermanagh_DCA.shp')
l_erne = gpd.read_file('data_files/ll_erne.shp')
buildings = gpd.read_file('data_files/Pointer_Fermanagh.shp')
lc = gpd.read_file('data_files/LCM_Fermanagh.shp')

flood_5m.to_crs(epsg = 2157)
hist_flood.to_crs(epsg = 2157)
boundary.to_crs(epsg = 2157)
l_erne.to_crs(epsg = 2157)
buildings.to_crs(epsg = 2157)
lc.to_crs(epsg = 2157)

myFig = plt.figure(figsize=(12, 12))  # create a figure of size 10x10 (representing the page size in inches)

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.
# be sure to fill in XX above with the correct number for the area we're working in.

ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.


outline_feature = ShapelyFeature(boundary['geometry'], myCRS, edgecolor='black', facecolor='white')
xmin, ymin, xmax, ymax = boundary.total_bounds # tells matplotlib to use boundary's total bounds
ax.add_feature(outline_feature) # adds boundary to map
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # sets map extent to extent of county boundary

print(lc.head())
num_lc = len(lc.LAND_COVER.unique())
print('No. lc classes: {}'.format(num_lc)) # counts how many unique land covers there are
list_lc = list(lc.LAND_COVER.unique())
print(list_lc) # prints a list of unique land covers

lc_colours = ['aqua','lightgreen','lawngreen','yellowgreen','sienna','lime','forestgreen','lime','olivedrab','darkgreen','saddlebrown','dimgray','olive','gray','lightgray','darkblue']

for i, name in enumerate(list_lc):
    lc_feat = ShapelyFeature(lc['geometry'][lc['LAND_COVER'] == name], myCRS,
                          edgecolor='black',
                          facecolor=lc_colours[i],
                          linewidth=0,
                          alpha=0.75)
    ax.add_feature(lc_feat)

flood_5m_feat = ShapelyFeature(flood_5m['geometry'], myCRS,
                            edgecolor='black',
                            facecolor = 'red',
                            hatch = 'xx',
                            linewidth=0.5)
ax.add_feature(flood_5m_feat)

l_erne_feat = ShapelyFeature(l_erne['geometry'], myCRS,
                            edgecolor='royalblue',
                            facecolor = 'royalblue',
                            linewidth=0.2)
ax.add_feature(l_erne_feat)
plt.savefig('Plot.png')


print(l_erne.head())
print(l_erne.TEMA.unique())

"""
print((sum(flood_5m.area))-(sum(l_erne.area)))

joined = gpd.sjoin(flood_5m, buildings, how = 'inner', lsuffix='left', rsuffix='right')
print(joined.head())

subset = gpd.sjoin(flood_5m, buildings, how='inner')

flood_geom = flood_5m['geometry'].values[0]
is_flooded = buildings['geometry'].within(flood_geom)

subset = buildings[is_flooded]

print(subset.groupby['TOWN'])
"""