import xarray as xr
import matplotlib.pyplot as plt

'''
avg_ishf sensible heat flux
avg_slhtf latent heat flux
'''

def plot_monthly_line():
    return

if __name__ == '__main__':
    # Define bounds 6.369454°S 106.655815°E
    lon_min, lon_max, lat_min, lat_max = (106.67, 106.97, -6.09, -6.35)

    # Open data
    file_name = './data/lab/surface_budget/vars_ERA5_1991-2020_mean_rates.nc'
    ds = xr.open_dataset(file_name)

    # Choose variables
    ds = ds[['avg_ishf', 'avg_slhtf', 'avg_snswrf', 'avg_snlwrf']]

    # Slice to Jakarta
    ds = ds.sel(
        latitude=slice(lat_min, lat_max),
        longitude=slice(lon_min, lon_max)
    )

    # Compute monthly
    ds_monthly = ds.groupby("valid_time.month").mean("valid_time")
    print(ds_monthly)

    # Initialize plot
    fig, ax = plt.subplots(figsize=(12, 9))

    # Flip sign
    ds_monthly['avg_ishf'] *= -1.0
    ds_monthly['avg_slhtf'] *= -1.0

    # Sensible heat cooling
    ds_monthly['avg_ishf'].plot(ax=ax, label='SH')
    ds_monthly['avg_slhtf'].plot(ax=ax, label='LH')
    (ds_monthly['avg_snswrf'] + ds_monthly['avg_snlwrf']).plot(ax=ax, label='Rs')
    plt.legend()
    plt.show()

    
    