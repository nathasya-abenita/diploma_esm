import xarray as xr
# import xarray_regrid 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np

def activate_geo_grid (ax):
    gl = ax.gridlines( draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--' ) 
    # Turn on/off labels for each side 
    gl.top_labels = False 
    gl.right_labels = False 
    # Format lon/lat labels 
    gl.xformatter = LongitudeFormatter() 
    gl.yformatter = LatitudeFormatter()

def compare_precipitation (path_model, varname_model, path_obs, varname_obs, model_name):
    
    # Read files
    ds_model = xr.open_dataset(path_model)
    ds_obs = xr.open_dataset(path_obs)
    print(ds_model.dims)
    print(ds_obs.dims)
    # ds_obs = ds_obs.rename({"longitude": "lon", "latitude": "lat"})

    # Organize
    pr = ds_model[varname_model] * -86400     #
    tp = ds_obs[varname_obs] * 1e3      # m to mm
    print(pr.shape)
    print(tp.shape)

    #%% MBE 

    # Compute bias
    bias_np = (pr.data - tp.data).mean(axis=0)

    bias = xr.DataArray(
        bias_np,
        dims=("lat", "lon"),
        coords={"lat": tp.lat.values, "lon": tp.lon.values},
        name="MBE"
    )

    # Plot
    fig = plt.figure(figsize=(10, 6)) 
    ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))
    cf = xr.plot.contourf(bias, ax=ax, x='lon', y='lat', transform=ccrs.PlateCarree(),
                        cbar_kwargs={'label': 'MBE (mm/d)', 'orientation': 'horizontal', 'pad': 0.05}, 
                        cmap='BrBG', levels=np.linspace(-10, 10, 11))

    # Add border
    ax.coastlines() 
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    # Add grid
    activate_geo_grid(ax)
    # Lay out
    ax.set_title(model_name)
    plt.tight_layout()

    # Save
    plt.savefig(f'output/cmip6/e_mbe_{model_name}.png')
    plt.close()

    #%% R
    
    # Means
    pr_mean = pr.data.mean(axis=0)
    tp_mean = tp.data.mean(axis=0)

    # Anomalies
    pr_anom = pr.data - pr_mean
    tp_anom = tp.data - tp_mean

    # Covariance
    cov = np.sum(pr_anom * tp_anom, axis=0)

    # Standard deviations
    std_pr = np.sqrt(np.sum(pr_anom**2, axis=0))
    std_tp = np.sqrt(np.sum(tp_anom**2, axis=0))

    # Pearson R
    R_np = cov / (std_pr * std_tp)

    bias = xr.DataArray(
        R_np,
        dims=("lat", "lon"),
        coords={"lat": tp.lat.values, "lon": tp.lon.values},
        name="R"
    )

    # Plot
    fig = plt.figure(figsize=(10, 6)) 
    ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))
    cf = xr.plot.pcolormesh(bias, ax=ax, x='lon', y='lat', transform=ccrs.PlateCarree(),
                        cbar_kwargs={'label': 'R', 'orientation': 'horizontal', 'pad': 0.05}, 
                        cmap='BrBG', levels=np.linspace(-1, 1, 11))


    # Add border
    ax.coastlines() 
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    # Add grid
    activate_geo_grid(ax)
    # Lay out
    ax.set_title(model_name)
    plt.tight_layout()

    # Save
    plt.savefig(f'output/cmip6/e_r_{model_name}.png')

if __name__ == '__main__':
    # File names
    path_model = r'./data/cmip6/historical/evspsbl_Amon_FIO-ESM-2-0_historical.nc'
    varname_model = 'evspsbl'
    path_obs = r'data/cmip6/era5_to_fio/evaporation.nc'
    varname_obs = 'e'
    model_name = 'FIO-ESM-2-0'

    # Call
    compare_precipitation (path_model, varname_model, path_obs, varname_obs, model_name)

    # File names
    path_model = r'./data/cmip6/historical/evspsbl_Amon_ACCESS-CM2_historical.nc'
    varname_model = 'evspsbl'
    path_obs = r'data/cmip6/era5_to_access/evaporation.nc'
    varname_obs = 'e'
    model_name = 'ACCESS-CM2'

    # Call
    compare_precipitation (path_model, varname_model, path_obs, varname_obs, model_name)