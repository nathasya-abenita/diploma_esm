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

def compare (path_hist, path_proj, varname, model_name):
    
    # Read files
    ds_hist = xr.open_dataset(path_hist)
    ds_proj = xr.open_dataset(path_proj)

    # Organize
    var_hist = ds_hist[varname] - 273
    var_proj = ds_proj[varname] - 273

    # Create stats

    mean_hist = xr.DataArray(
        var_hist.mean(axis=0),
        dims=("lat", "lon"),
        coords={"lat": var_hist.lat.values, "lon": var_hist.lon.values},
        name="mean"
    )

    mean_proj = xr.DataArray(
        var_proj.mean(axis=0),
        dims=("lat", "lon"),
        coords={"lat": var_hist.lat.values, "lon": var_hist.lon.values},
        name="mean"
    )

    mean_diff = mean_proj - mean_hist


    # --- Plot ---
    fig, axes = plt.subplots(
        1, 3,
        figsize=(18, 5),
        subplot_kw={"projection": ccrs.Mollweide(central_longitude=120)} # 180 for the usual Pacific center
    )

    # Suggested precipitation ranges (adjust as needed)
    vmax = np.nanpercentile(mean_proj.values, 99)
    vmin = 20
    levels_mean = np.linspace(20, 30, 11)

    diff_max = np.nanpercentile(np.abs(mean_diff.values), 99)
    levels_diff = np.linspace(0, 4, 11)

    # Plot settings
    datasets = [mean_hist, mean_proj, mean_diff]
    titles = ["Historical Mean (1981-2010)", "SSP5-8.5 Mean (2051-2080)", "Change"]
    cmaps = ["YlOrRd", "YlOrRd", "OrRd"]
    levels_list = [levels_mean, levels_mean, levels_diff]

    for ax, data, title, cmap, levels in zip(axes, datasets, titles, cmaps, levels_list):
        cf = xr.plot.contourf(
            data,
            ax=ax,
            x='lon', y='lat',
            transform=ccrs.PlateCarree(),
            cmap=cmap,
            levels=levels,
            add_colorbar=False
        )

        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        # activate_geo_grid(ax)
        ax.set_title(title)
        ax.set_extent([90, 150, -15, 10], crs=ccrs.PlateCarree()) # Indonesian extent

        # Individual colorbar for each subplot
        cbar = fig.colorbar(
            cf, ax=ax,
            orientation='horizontal',
            pad=0.05,
            label="deg C"
        )
    plt.suptitle(model_name, y=0.92)
    plt.tight_layout()

    # Save
    plt.savefig(f'output/cmip6/projection_tas_{model_name}.png', dpi=300)
    plt.close()
    plt.close()

if __name__ == '__main__':
    # File names
    path_hist = r'./data/cmip6/historical/tas_Amon_FIO-ESM-2-0_historical.nc'
    path_proj = r'data/cmip6/ssp585/tas_Amon_FIO-ESM-2-0_ssp585_r1i1p1f1_gn_20510116-20801216.nc'
    varname_model = 'tas'
    model_name = 'FIO-ESM-2-0'

    # Call
    compare (path_hist, path_proj, varname_model, model_name)

     # File names
    path_hist = r'./data/cmip6/historical/tas_Amon_ACCESS-CM2_historical.nc'
    path_proj = r'data/cmip6/ssp585/tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_20510116-20801216.nc'
    varname_model = 'tas'
    model_name = 'ACCESS-CM2'

    # Call
    compare (path_hist, path_proj, varname_model, model_name)