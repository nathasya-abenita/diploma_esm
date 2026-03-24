import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Indonesia domain
INDO_EXTENT = [90, 150, -15, 10]

def seasonal_mean(ds, varname, season):
    """Compute seasonal mean for DJF or JJA."""
    return (
        ds[varname]
        .sel(time=ds['time'].dt.season == season)
        .mean('time')
    )

def compare_seasonal_change(path_hist, path_proj, varname):
    """Return DJF and JJA mean changes for one model."""
    ds_hist = xr.open_dataset(path_hist)
    ds_proj = xr.open_dataset(path_proj)

    # Cut to Indonesia first (saves memory)
    ds_hist = ds_hist.sel(lon=slice(INDO_EXTENT[0], INDO_EXTENT[1]),
                          lat=slice(INDO_EXTENT[2], INDO_EXTENT[3]))
    ds_proj = ds_proj.sel(lon=slice(INDO_EXTENT[0], INDO_EXTENT[1]),
                          lat=slice(INDO_EXTENT[2], INDO_EXTENT[3]))

    # Compute seasonal means
    hist_DJF = seasonal_mean(ds_hist, varname, "DJF")
    hist_JJA = seasonal_mean(ds_hist, varname, "JJA")

    proj_DJF = seasonal_mean(ds_proj, varname, "DJF")
    proj_JJA = seasonal_mean(ds_proj, varname, "JJA")

    # Compute changes
    diff_DJF = proj_DJF - hist_DJF
    diff_JJA = proj_JJA - hist_JJA

    return diff_DJF, diff_JJA


def plot_two_models(model_results, model_names):
    """Plot 2 rows (models) × 2 columns (DJF, JJA)."""

    fig, axes = plt.subplots(
        2, 2,
        figsize=(14, 10),
        subplot_kw={"projection": ccrs.PlateCarree()}
    )

    seasons = ["DJF", "JJA"]

    # Determine global color scale
    all_values = []
    for diffs in model_results:
        for d in diffs:
            all_values.append(d.values)

    vmax = np.nanpercentile(np.abs(np.concatenate([v.flatten() for v in all_values])), 98)
    levels = np.linspace(0.5, 3.5, 9)

    for i, (diff_DJF, diff_JJA) in enumerate(model_results):
        for j, diff in enumerate([diff_DJF, diff_JJA]):
            ax = axes[i, j]

            cf = diff.plot.contourf(
                ax=ax,
                transform=ccrs.PlateCarree(),
                cmap="OrRd",
                levels=levels,
                add_colorbar=False
            )

            ax.coastlines()
            ax.add_feature(cfeature.BORDERS, linewidth=0.5)
            ax.set_extent(INDO_EXTENT, crs=ccrs.PlateCarree())

            ax.set_title(f"{model_names[i]} – {seasons[j]} Change")

            # Add colorbar
            cbar = fig.colorbar(cf, ax=ax, orientation="horizontal", pad=0.05)
            cbar.set_label("deg")
    plt.suptitle('Historical (1981-2010) vs SSP5-8.5 (2051-2080) Mean', y=0.92)
    plt.tight_layout()
    plt.savefig("output/cmip6/tas_seasonal_change.png", dpi=300)
    plt.close()

if __name__ == "__main__":

    models = [
        ("./data/cmip6/historical/tas_Amon_FIO-ESM-2-0_historical.nc",
         "data/cmip6/ssp585/tas_Amon_FIO-ESM-2-0_ssp585_r1i1p1f1_gn_20510116-20801216.nc",
         "FIO-ESM-2-0"),

        ("./data/cmip6/historical/tas_Amon_ACCESS-CM2_historical.nc",
         "data/cmip6/ssp585/tas_Amon_ACCESS-CM2_ssp585_r1i1p1f1_gn_20510116-20801216.nc",
         "ACCESS-CM2")
    ]

    varname = "tas"

    results = []
    names = []

    for hist, proj, name in models:
        diff_DJF, diff_JJA = compare_seasonal_change(hist, proj, varname)
        results.append((diff_DJF, diff_JJA))
        names.append(name)

    plot_two_models(results, names)
