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

def compute_monthly(ds):
    ds_monthly = ds.groupby("valid_time.month").mean("valid_time")

    # Sign convention (upward heat flux positive)
    ds_monthly["avg_ishf"] = -ds_monthly["avg_ishf"]
    ds_monthly["avg_slhtf"] = -ds_monthly["avg_slhtf"]
    ds_monthly["avg_snlwrf"] = -ds_monthly["avg_snlwrf"]

    # Net radiation
    ds_monthly["Rs"] = ds_monthly["avg_snswrf"] - ds_monthly["avg_snlwrf"]

    # Heat storage
    ds_monthly["Storage"] = ds_monthly["Rs"] - (ds_monthly["avg_ishf"] + ds_monthly["avg_slhtf"])

    return ds_monthly


def plot_monthly_line(ds_monthly):
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
    plt.show()


if __name__ == "__main__":
    # Data location
    file_name = "./data/lab/surface_budget/vars_ERA5_1991-2020_mean_rates.nc"

    # Jakarta bounds
    bounds = dict(
        lon_min=106.67,
        lon_max=106.97,
        lat_min=-6.09,
        lat_max=-6.35
    )
    ds = load_dataset(file_name)
    ds = subset_region(ds, bounds)
    ds_monthly = compute_monthly(ds)
    plot_monthly_line(ds_monthly)