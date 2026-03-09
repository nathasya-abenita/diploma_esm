#%%

import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import contextily as ctx

#%% Inputs

lon = 106.8      # ERA5 longitude
lat = -6.25      # ERA5 latitude
res = 0.25      # ERA5 grid resolution (°)

#%% Build grid cell polygon

lon_min = lon - res / 2
lon_max = lon + res / 2
lat_min = lat - res / 2
lat_max = lat + res / 2

poly = Polygon([
    (lon_min, lat_min),
    (lon_min, lat_max),
    (lon_max, lat_max),
    (lon_max, lat_min)
])

gdf = gpd.GeoDataFrame({"geometry": [poly]}, crs="EPSG:4326")


# Reproject for contextily
gdf_web = gdf.to_crs(epsg=3857)


#%% Plot

# Initialize
fig, ax = plt.subplots(figsize=(8, 8))

# Plot the grid cell
gdf_web.boundary.plot(ax=ax, linewidth=2, edgecolor="red")
gdf_web.plot(ax=ax, alpha=0.3, color="red")

# Adjust limits
alpha = 0.3
xmin, ymin, xmax, ymax = gdf_web.total_bounds
delta_x, delta_y = xmax - xmin, ymax - ymin
ax.set_xlim([xmin - delta_x * alpha, xmax + delta_x * alpha])
ax.set_ylim([ymin - delta_y * alpha, ymax + delta_y * alpha])

# Add basemap
ctx.add_basemap(ax)

ax.set_title("Chosen Grid Cell(s)")
ax.set_axis_off()

plt.show()