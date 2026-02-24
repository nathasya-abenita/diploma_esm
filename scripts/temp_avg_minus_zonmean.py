#%% Import packages
import xarray as xr

#%% Processing
if __name__ == '__main__':
    # Read data
    ds_avg = xr.open_dataset('./data/lab/t2m-avg.nc')
    ds_zonmean = xr.open_dataset('./data/lab/t2m-avg-zonmean.nc').squeeze('lon')
    ds_avg = ds_avg.rename({'longitude': 'lon', 'latitude': 'lat'})

    # Compute difference
    da_anomaly = ds_avg['t2m'] - ds_zonmean['t2m']

    # Save
    ds_anomaly = da_anomaly.to_dataset(name='t2m') # Dataset ds_new.to_netcdf("t2m.nc")
    ds_anomaly.to_netcdf('./data/lab/t2m-anomaly.nc', mode='w')