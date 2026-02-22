#%% Import packages
import xarray as xr
import matplotlib.pyplot as plt

#%% Long wave plot

# Read data
ds = xr.open_dataset('./data/lab/net-long-annual-mean.nc')

# Plot data
fig = ds['avg_snlwrf'].plot()
plt.title('Annual means (1991-2021)')
plt.savefig('./output/lab1/long-annual-mean.png')

#%% Short wave plot

# Read data
ds = xr.open_dataset('./data/lab/net-short-annual-mean.nc')

# Plot data
fig = ds['avg_snswrf'].plot()
plt.title('Annual means (1991-2021)')
plt.savefig('./output/lab1/short-annual-mean.png')