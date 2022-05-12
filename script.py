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
np.set_printoptions(linewidth = desired_width)
pd.set_option('display.max_columns',40) # this block of code modified from Stack Overflow tells PyCharm to show you the whole head of a table, not just 5 columns


flood_5m = gpd.read_file('data_files/flood_5m.shp')
hist_flood = gpd.read_file('data_files/hist_flood.shp')
boundary = gpd.read_file('data_files/Fermanagh_DCA.shp')
l_erne = gpd.read_file('data_files/ll_erne.shp')
buildings = gpd.read_file('data_files/Pointer_Fermanagh.shp')
lc = gpd.read_file('data_files/LCM_Fermanagh.shp') # read the data files
roads = gpd.read_file('data_files/Fermanagh roads.shp')

flood_5m.to_crs(epsg = 2157)
hist_flood.to_crs(epsg = 2157)
boundary.to_crs(epsg = 2157)
l_erne.to_crs(epsg = 2157)
buildings.to_crs(epsg = 2157)
lc.to_crs(epsg = 2157) # convert files to Irish Transverse Mercator



"""
area_flooded_5m = sum((flood_5m.area)-(sum(l_erne.area))) # the area of land that will be flooded in Lower Lough Erne experiences a 5m flood
area_flooded_hist = sum((hist_flood.area)-(sum(l_erne.area))) # the area of land that was flooded in Lower Lough Erne historical flood event

print('Land inundated during 5m flood: {}'.format(area_flooded_5m)) #print the above value
print('Land inundated during historical flood event: {}'.format(area_flooded_hist)) # print the above value


flood_geom = flood_5m['geometry'].values[0] # select flood polygon
is_flooded = buildings['geometry'].within(flood_geom) # select all buildings within fLood polygon

count_buildings = buildings[is_flooded]['BUILDING_S'].size # count number of buildings inundated during 5m flood
print('Buildings inundated during 5m flood: {}'.format(count_buildings))

joined = gpd.sjoin(flood_5m, buildings, how = 'inner', lsuffix='left', rsuffix='right')
#print(joined.head())

subset = gpd.sjoin(flood_5m, buildings, how='inner')

"""

def generate_handles(labels, colors, edge='black', alpha=1):
    lcol = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lcol], edgecolor=edge, alpha=alpha))
    return handles
"""Generate Matplotlib handles for map legend.

Extracts labels from given list of handles in string format.
Iterates over labels assigning each one a rectangle of colour.
Colours can be assigned in previous step or can be added on the fly.

Returns a set of handles to be added to the map legend.
"""

def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    ax.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    ax.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
    ax.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
    ax.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)
"""Creates a scale bar to be added to the upper right corner of the map


"""

myFig = plt.figure(figsize=(12, 12))  # create a figure of size 12x12 inches

myCRS = ccrs.UTM(29) # transform data to Ireland section of Universal Transverse Mercator 

ax = plt.axes(projection=ccrs.Mercator())  # create an object with axes in the figure with Mercator projection to plot map data

outline_feature = ShapelyFeature(boundary['geometry'], myCRS, edgecolor='black', facecolor='white') # plot the county outline
xmin, ymin, xmax, ymax = boundary.total_bounds # tells geopandas to use boundary's total bounds
ax.add_feature(outline_feature) # adds boundary to map
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # sets map extent to extent of county boundary

print(lc.head())
num_lc = len(lc.LAND_COVER.unique())
print('No. lc classes: {}'.format(num_lc)) # counts how many unique land covers there are
list_lc = list(lc.LAND_COVER.unique())
print(list_lc) # prints a list of unique land covers

lc_colours = ['aqua','lightgreen','lawngreen','yellowgreen','sienna','lime','forestgreen','limegreen','olivedrab','darkgreen','saddlebrown','dimgray','olive','gray','lightgray','darkblue'] #list of colours for land cover in order of those listed in output by above step

for i, name in enumerate(list_lc):
    lc_feat = ShapelyFeature(lc['geometry'][lc['LAND_COVER'] == name], myCRS, # iterate over and assign a new colour to each of the land cover classes and create land cover feature object
                          edgecolor='black', # plot outline in black
                          facecolor=lc_colours[i], # plot the land covers in their unique colours assigned above
                          linewidth=0, # don't put outlines on land cover polygons
                          alpha=1) # colour saturation
    ax.add_feature(lc_feat) # plot the above on the axis

flood_5m_feat = ShapelyFeature(flood_5m['geometry'], myCRS, # create feature object of a 5m flood event of Lower Lough Erne
                            edgecolor='black', # plot outline in black
                            facecolor = 'red', # plot the flood in red
                            hatch = 'xx', # with a hatch to distinguish from land cover
                            linewidth=0.5, # width of bounding lines
                            alpha = 0.75)
ax.add_feature(flood_5m_feat) # plot the above on the axis

l_erne_feat = ShapelyFeature(l_erne['geometry'], myCRS, # create a feature object of Lower Lough Erne
                            edgecolor='royalblue', # plot outline in royal blue
                            facecolor = 'royalblue',  # plot Lough Erne in royal blue
                            linewidth=0.2, # width of bounding lines
                            alpha = 0.75)
ax.add_feature(l_erne_feat) # plot the above on the axis

lc_handles = generate_handles(lc.LAND_COVER.unique(), lc_colours, alpha=1)
l_erne_handle = generate_handles(['l_erne'], ['royalblue'])
flood_5m_handle = generate_handles(['flood_5m'], ['red'])

handles = lc_handles + l_erne_handle + flood_5m_handle
labels = list_lc + ['Lough Erne', '5m Flood']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                 fontsize=10, loc='lower right', frameon=True, framealpha=1)
scale_bar(ax)
plt.savefig('Plot.png') # save the plotted figure


