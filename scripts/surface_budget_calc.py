
import xarray as xr

"""
ERA5 variables
avg_ishf   : sensible heat flux
avg_slhtf  : latent heat flux
avg_snswrf : net shortwave radiation
avg_snlwrf : net longwave radiation
"""

if __name__ == '__main__':
    # Read data
    ds = xr.open_dataset(r'./data/lab/surface_budget/surface_budget_timmean.nc')

    # Compute
    ds['rs'] = ds['avg_snswrf'] + ds['avg_snlwrf'] # net radiation
    ds['gs']= ds['rs'] + ds['avg_ishf'] + ds['avg_slhtf'] # storage

    # Save
    ds.to_netcdf('./data/lab/surface_budget/surface_budget_timmean_complete.nc', mode='w')