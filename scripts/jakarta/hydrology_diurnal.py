import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from module import representative_cell

def prepare_ds (ds, time_min, time_max):
    ds_day = ds.assign_coords(valid_time = ds.valid_time + np.timedelta64(7, "h"))
    ds_day = ds_day.sel(valid_time=slice(time_min, time_max))
    ds_day = ds_day.groupby("valid_time.hour").mean()
    return ds_day

def plot_hourly_line(ds, ds_t2m, ds_swvl_tcc, ds_ro, time_min, time_max, out_file_name, title):

    ds_day = prepare_ds(ds, time_min, time_max)
    ds_t2m = prepare_ds(ds_t2m, time_min, time_max)
    ds_ro = prepare_ds(ds_ro, time_min, time_max)
    ds_swvl_tcc = prepare_ds(ds_swvl_tcc, time_min, time_max)

    # Initialize figure
    fig, (ax, ax_bottom) = plt.subplots(
    2, 1, figsize=(12, 10), sharex=True,
    gridspec_kw={'height_ratios': [2, 1]}
    )

    # Main hydrology cycle
    ax.plot(ds_day['tp'], 'b--', label='P')
    ax.plot(ds_day['e'], 'r--', label='E')
    ax.plot(ds_day['pev'], 'k', label='PET')
    ax.plot(ds_ro['ro'], '--', color='gray', label='ΔF')

    # Create second y-axis for temperature
    ax2 = ax.twinx()
    ax2.plot(ds_t2m['t2m'], color='darkred', linewidth=2.5, marker='o', label='Temperature (°C)')

    # BOTTOM PLOT
    ax_bottom.plot(ds_swvl_tcc['swvl1'], color='purple', label='Surface moisture')
    ax_bottom.plot(ds_swvl_tcc['tcc'], color='gray', label='Total cloud cover')
    ax_bottom.set_ylabel('unitless')
    ax_bottom.set_ylim(0, 1)
    ax_bottom.set_xlabel('month')
    ax_bottom.legend()

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

    # Moisture and runoff for both data

    ds_swvl_tcc = xr.open_dataset(r'data/lab/hourly_surface_budget/moisture_and_runoff/data_stream-oper_stepType-instant.nc')
    ds_ro = xr.open_dataset(r'data/lab/hourly_surface_budget/moisture_and_runoff/data_stream-oper_stepType-accum.nc')
    
    ds_swvl_tcc = representative_cell(ds_swvl_tcc, lon, lat)
    ds_ro = representative_cell(ds_ro, lon, lat)

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
    ds_ro['ro'] *= 1e3

    plot_hourly_line(ds, ds_t2m, ds_swvl_tcc, ds_ro, time_min='2022-10-01 00:00', time_max='2022-10-31 23:00',
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

    plot_hourly_line(ds, ds_t2m, ds_swvl_tcc, ds_ro, time_min='2022-05-01 00:00', time_max='2022-05-31 23:00',
                     out_file_name='./output/hydrology/may_diurnal_cycle.png',
                     title = 'May 2022')
