import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

"""
ERA5 variables
avg_ishf   : sensible heat flux
avg_slhtf  : latent heat flux
avg_snswrf : net shortwave radiation
avg_snlwrf : net longwave radiation
"""

def load_dataset(file_name):
    ds = xr.open_dataset(file_name)

    variables = [
        "avg_ishf",
        "avg_slhtf",
        "avg_snswrf",
        "avg_snlwrf"
    ]
        
    return ds[variables]

def compute_fluxes(ds):

    # Sign convention (upward heat flux positive)
    ds["avg_ishf"] = -ds["avg_ishf"]
    ds["avg_slhtf"] = -ds["avg_slhtf"]
    ds["avg_snlwrf"] = -ds["avg_snlwrf"]

    # Net radiation
    ds["Rs"] = ds["avg_snswrf"] - ds["avg_snlwrf"]

    # Heat storage
    ds["Storage"] = ds["Rs"] - (ds["avg_ishf"] + ds["avg_slhtf"])

    return ds


def plot_monthly_line(ds_monthly, out_file_name):
    fig, ax = plt.subplots(figsize=(12, 9))

    ds_monthly["Rs"].plot(ax=ax, label="Net Radiation (Rs)", color='k')
    ds_monthly['avg_snswrf'].plot(ax=ax, label="Net Shortwave Radiation", color='yellow', alpha=0.85)
    ds_monthly['avg_snlwrf'].plot(ax=ax, label="Net Longwave Radiation", color='tab:green', alpha=0.85)

    ds_monthly["avg_ishf"].plot(ax=ax, label="Sensible Heat (SH)", color='r', linestyle='--')
    ds_monthly["avg_slhtf"].plot(ax=ax, label="Latent Heat (LH)", color='b', linestyle='--')
    ds_monthly["Storage"].plot(ax=ax, label="Heat Storage", color='orange', linestyle='--')

    # Activate texts
    ax.set_ylabel("W m$^{-2}$")
    ax.set_title("Monthly Mean Surface Heat Fluxes (ERA5, 1991-2020) - Jakarta")
    ax.legend()

    # Activate monthly index name
    month_labels = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
    ]
    ax.set_xticks(range(1, 12+1))
    ax.set_xticklabels(month_labels)

    plt.grid()
    plt.savefig(out_file_name)

def plot_hourly_line(ds, time_min, time_max, out_file_name, title):

    ds = ds.assign_coords(valid_time = ds.valid_time + np.timedelta64(7, "h"))
    ds_day = ds.sel(valid_time=slice(time_min, time_max))
    # Compute diurnal cycle (average by hour)
    ds_day = ds_day.groupby("valid_time.hour").mean()

    fig, ax = plt.subplots(figsize=(12, 6))

    ds_day["Rs"].plot(ax=ax, label="Rs", color='k')
    ds_day['avg_snswrf'].plot(ax=ax, label="Net Shortwave Radiation", color='yellow', alpha=0.85)
    ds_day['avg_snlwrf'].plot(ax=ax, label="Net Longwave Radiation", color='tab:green', alpha=0.85)


    ds_day["avg_ishf"].plot(ax=ax, label="SH", color='r', linestyle='--')
    ds_day["avg_slhtf"].plot(ax=ax, label="LH", color='b', linestyle='--')
    ds_day["Storage"].plot(ax=ax, label="Storage", color='orange', linestyle='--')

    ax.set_xlabel("Local Hour")
    ax.set_ylabel("W m$^{-2}$")
    ax.set_title(f"Surface Energy Budget (ERA5) - Jakarta - {title}")

    ax.legend()
    ax.grid()
    plt.savefig(out_file_name)

def representative_cell(ds, lon, lat):
    """
    Return a representative time series at (lon, lat) by:
    1. Finding the nearest grid cell
    2. Taking the 2×2 neighborhood around it
    3. Averaging those 4 values
    """

    # 1. Find nearest grid cell
    pt = ds.sel(longitude=lon, latitude=lat, method="nearest")
    lon0 = float(pt.longitude)
    lat0 = float(pt.latitude)

    # 2. Get index of that grid cell
    ilon = ds.longitude.to_index().get_loc(lon0)
    ilat = ds.latitude.to_index().get_loc(lat0)

    # 3. Select the 2×2 neighborhood
    ds4 = ds.isel(
        longitude=slice(ilon, ilon + 2),
        latitude=slice(ilat, ilat + 2)
    )
    # print(ds4.coords)

    # 4. Average to get one representative time series
    return ds4.mean(dim=("latitude", "longitude"))
