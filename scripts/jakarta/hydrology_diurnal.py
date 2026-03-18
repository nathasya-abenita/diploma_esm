import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from module import representative_cell

def plot_hourly_line(ds, ds_t2m, time_min, time_max, out_file_name, title):

    ds_day = ds.assign_coords(valid_time = ds.valid_time + np.timedelta64(7, "h"))
    ds_day = ds_day.sel(valid_time=slice(time_min, time_max))
    ds_day = ds_day.groupby("valid_time.hour").mean()

    ds_t2m = ds_t2m.assign_coords(valid_time = ds.valid_time + np.timedelta64(7, "h"))
    ds_t2m = ds_t2m.sel(valid_time=slice(time_min, time_max))
    ds_t2m = ds_t2m.groupby("valid_time.hour").mean()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(ds_day['tp'], 'b--', label='P')
    ax.plot(ds_day['e'], 'r--', label='E')
    ax.plot(ds_day['pev'], 'k', label='PET')

    # Create second y-axis for temperature
    ax2 = ax.twinx()
    ax2.plot(ds_t2m['t2m'], color='darkred', linewidth=2.5, marker='o', label='Temperature (°C)')

    ax.set_xlabel('Local Hour')
    ax.set_ylabel('mm/h')
    ax2.set_ylabel('Surface temperature (°C)', color='darkred')
    ax.legend(loc='upper right'); ax2.legend(loc='upper left')
    ax.set_title(f"Hydrological Cycle (ERA5) - Jakarta - {title}")

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
    lon, lat = (106.8229, -6.1944) # jakarta center

    #%% Oct 2022

    file_name = "./data/lab/hourly_surface_budget/oct_2022/data_stream-oper_stepType-accum.nc"
    ds = xr.open_dataset(file_name)
    ds = representative_cell(ds, lon, lat)

    file_name = "./data/lab/hourly_surface_budget/oct_2022/data_stream-oper_stepType-instant.nc"
    ds_t2m = xr.open_dataset(file_name)
    ds_t2m = representative_cell(ds_t2m, lon, lat)

    ds['tp'] = ds['tp'] * 1e3 # m to mm
    ds['e'] = ds['e'] * -1e3 # m to mm, evapotranspiration to be positive
    ds['pev'] = ds['pev'] * -1e3 # m to mm
    ds_t2m['t2m'] = ds_t2m['t2m'] - 273.15 # k to deg c

    plot_hourly_line(ds, ds_t2m, time_min='2022-10-01 00:00', time_max='2022-10-31 23:00',
                     out_file_name='./output/hydrology/oct_diurnal_cycle.png',
                     title = 'Oct 2022')
    
    #%% May 2022

    file_name = "./data/lab/hourly_surface_budget/may_2022/data_stream-oper_stepType-accum.nc"
    ds = xr.open_dataset(file_name)
    ds = representative_cell(ds, lon, lat)

    file_name = "./data/lab/hourly_surface_budget/may_2022/data_stream-oper_stepType-instant.nc"
    ds_t2m = xr.open_dataset(file_name)
    ds_t2m = representative_cell(ds_t2m, lon, lat)

    ds['tp'] = ds['tp'] * 1e3 # m to mm
    ds['e'] = ds['e'] * -1e3 # m to mm, evapotranspiration to be positive
    ds['pev'] = ds['pev'] * -1e3 # m to mm
    ds_t2m['t2m'] = ds_t2m['t2m'] - 273.15 # k to deg c

    plot_hourly_line(ds, ds_t2m, time_min='2022-05-01 00:00', time_max='2022-05-31 23:00',
                     out_file_name='./output/hydrology/may_diurnal_cycle.png',
                     title = 'May 2022')
