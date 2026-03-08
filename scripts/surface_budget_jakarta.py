import xarray as xr
import matplotlib.pyplot as plt

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


def subset_region(ds, bounds):
    return ds.sel(
        latitude=slice(bounds["lat_min"], bounds["lat_max"]),
        longitude=slice(bounds["lon_min"], bounds["lon_max"])
    )

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

def plot_hourly_line(ds, time_min, time_max, out_file_name):

    ds_day = ds.sel(valid_time=slice(time_min, time_max))

    fig, ax = plt.subplots(figsize=(12, 6))

    ds_day["Rs"].plot(ax=ax, label="Rs", color='k')
    ds_day['avg_snswrf'].plot(ax=ax, label="Net Shortwave Radiation", color='yellow', alpha=0.85)
    ds_day['avg_snlwrf'].plot(ax=ax, label="Net Longwave Radiation", color='tab:green', alpha=0.85)


    ds_day["avg_ishf"].plot(ax=ax, label="SH", color='r', linestyle='--')
    ds_day["avg_slhtf"].plot(ax=ax, label="LH", color='b', linestyle='--')
    ds_day["Storage"].plot(ax=ax, label="Storage", color='orange', linestyle='--')

    ax.set_xlabel("Hour")
    ax.set_ylabel("W m$^{-2}$")
    ax.set_title(f"Surface Energy Budget (ERA5) - Jakarta")

    # ax.set_xticks(ds_day.valid_time)
    # # Format x-axis to show only hours
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    # # Optional: set major ticks every hour
    # ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    ax.legend()
    ax.grid()
    plt.savefig(out_file_name)

if __name__ == "__main__":
    # Jakarta bounds
    bounds = dict(
        lon_min=106.67,
        lon_max=106.97,
        lat_min=-6.09,
        lat_max=-6.35
    )

    #%% Annual cycle

    file_name = "./data/lab/surface_budget/vars_ERA5_1991-2020_mean_rates.nc"
    ds = load_dataset(file_name)
    ds = subset_region(ds, bounds)
    ds = ds.groupby("valid_time.month").mean("valid_time") # compute monthly mean
    ds_monthly = compute_fluxes(ds)
    plot_monthly_line(ds_monthly, 
                      out_file_name='./output/surface_budget/annual_cycle.png')

    #%% Diurnal cycle

    file_name = "./data/lab/hourly_surface_budget/dec_2022.nc"
    ds = load_dataset(file_name)
    ds = subset_region(ds, bounds)
    ds = compute_fluxes(ds)
    plot_hourly_line(ds, time_min='2022-12-29 00:00', time_max='2022-12-29 23:00',
                     out_file_name='./output/surface_budget/dec_diurnal_cycle.png')
    
    file_name = "./data/lab/hourly_surface_budget/oct_2022.nc"
    ds = load_dataset(file_name)
    ds = subset_region(ds, bounds)
    ds = compute_fluxes(ds)
    plot_hourly_line(ds, time_min='2022-10-06 00:00', time_max='2022-10-12 23:00',
                     out_file_name='./output/surface_budget/oct_diurnal_cycle.png')