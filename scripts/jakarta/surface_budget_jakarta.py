import xarray as xr
import matplotlib.pyplot as plt
from module import load_dataset, representative_cell, compute_fluxes, plot_hourly_line, plot_monthly_line

if __name__ == "__main__":
    # Jakarta bounds
    bounds = dict(
        lon_min=106.67,
        lon_max=106.97,
        lat_min=-6.09,
        lat_max=-6.35
    )
    lon, lat = (106.8229, -6.1944) # jakarta center

    #%% Annual cycle

    file_name = "./data/lab/surface_budget/vars_ERA5_1991-2020_mean_rates.nc"
    ds = load_dataset(file_name)
    ds = representative_cell(ds, lon, lat)
    ds = ds.groupby("valid_time.month").mean("valid_time") # compute monthly mean
    ds_monthly = compute_fluxes(ds)
    plot_monthly_line(ds_monthly, 
                      out_file_name='./output/surface_budget/annual_cycle.png')

    #%% Diurnal cycle

    file_name = "./data/lab/hourly_surface_budget/oct_2022/data_stream-oper_stepType-avg.nc"
    ds = load_dataset(file_name)
    ds = representative_cell(ds, lon, lat)
    ds = compute_fluxes(ds)
    plot_hourly_line(ds, time_min='2022-10-06 00:00', time_max='2022-10-12 23:00',
                     out_file_name='./output/surface_budget/oct_diurnal_cycle.png',
                     title = 'Oct 2022')
    
    file_name = "./data/lab/hourly_surface_budget/may_2022/data_stream-oper_stepType-avg.nc"
    ds = load_dataset(file_name)
    ds = representative_cell(ds, lon, lat)
    ds = compute_fluxes(ds)
    plot_hourly_line(ds, time_min='2022-05-01 00:00', time_max='2022-05-31 23:00',
                     out_file_name='./output/surface_budget/may_diurnal_cycle.png', 
                     title = 'May 2022')