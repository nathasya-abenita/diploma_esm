import numpy as np
import geopandas as gpd
import regionmask

def subset_region(ds, bounds):
    return ds.sel(
        latitude=slice(bounds["lat_min"], bounds["lat_max"]),
        longitude=slice(bounds["lon_min"], bounds["lon_max"])
    )

def subset_with_regionmask(ds, shp_path, print_coords=False):
    gdf = gpd.read_file(shp_path)

    # Create mask (lat x lon)
    mask = regionmask.mask_geopandas(gdf, ds.longitude, ds.latitude)

    # Boolean mask: True inside polygon
    inside_mask = mask == 0

    # Apply mask directly (keeps grid structure but removes outside points)
    ds_sub = ds.where(inside_mask, drop=True)

    if print_coords:
        inside = np.where(inside_mask)
        print("Selected coordinate pairs (lon, lat):")
        for i, j in zip(*inside):
            print(float(ds.longitude[j]), float(ds.latitude[i]))

    return ds_sub


def fldmean(ds, varname):
    lat = ds['latitude']
    weights = np.cos(np.deg2rad(lat))
    weights.name = "weights"

    da = ds[varname]  # extract the DataArray
    return da.weighted(weights).mean(dim=("latitude", "longitude"))
