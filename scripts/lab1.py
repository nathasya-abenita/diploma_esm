"""
Author: Nathasya Christien
Starting Date: 2026-02-22
Description: Plotting ERA5 and temperature data for lab #1
""" 

#%% Import packages
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import cartopy.crs as ccrs 
import cartopy.feature as cfeature

def plot_contourf (file_name, var_name, title, output_file_name, levels=None, xlabel=None, ylabel=None, unit=None, operator=None):
    # Read data
    ds = xr.open_dataset(file_name)
    
    # Apply operation to variable if needed
    if operator != None:
        ds[var_name] = operator(ds[var_name])

    # Color bar label
    if unit == None:
        cbar_label = rf"{ds[var_name].attrs['long_name']} ({ds[var_name].attrs['units']})"
    else:
        cbar_label = rf"{ds[var_name].attrs['long_name']} ({unit})"

    # Build a discrete version of coolwarm
    base = plt.get_cmap('coolwarm') 
    colors = base(np.linspace(0, 1, levels)) 
    # Find the index corresponding to value 0 
    vmin = ds[var_name].min(); vmax = ds[var_name].max() 
    zero_pos = int((0 - vmin) / (vmax - vmin) * (levels - 1)) 
    # Set that color to white 
    colors[zero_pos] = np.array([1, 1, 1, 1]) 
    # Create new colormap 
    new_cmap = mcolors.ListedColormap(colors)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6)) 
    xr.plot.contourf(ds[var_name], x='valid_time', y='lat', cbar_kwargs={'label': cbar_label}, cmap=new_cmap, levels=levels)
    ax.set_title(title)

    # Check if the x-axis coordinate is datetime-like 
    xcoord = ds[var_name].coords['valid_time'] 
    if np.issubdtype(xcoord.dtype, np.datetime64): 
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # Set labels
    if xlabel != None:
        ax.set_xlabel(xlabel)
    if ylabel != None:
        ax.set_ylabel(ylabel)
    plt.savefig(output_file_name)


def plot_map (file_name, var_name, title, output_file_name, operator=None):
    # Read data 
    ds = xr.open_dataset(file_name)
    
    # Apply operation to variable if needed
    if operator != None:
        ds[var_name] = operator(ds[var_name])

    # Create figure with Cartopy projection 
    fig = plt.figure(figsize=(10, 6)) 
    ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180)) 

    # Color bar label
    cbar_label = rf"{ds[var_name].attrs['long_name']} ({ds[var_name].attrs['units']})"

    # Plot variable
    p = ds[var_name].plot(ax=ax, 
                            transform=ccrs.PlateCarree(),
                            cbar_kwargs={
                                    'label': cbar_label, 
                                    'orientation': 'horizontal', 
                                    'pad': 0.05
                                        },
                            cmap='coolwarm')
    ax.coastlines() 
    ax.add_feature(cfeature.BORDERS, linewidth=0.5) 
    ax.set_title(title)
    plt.savefig(output_file_name)

if __name__ == '__main__':

    # # Long wave at surface plot
    # plot_map(file_name = './data/lab/net-long-annual-mean.nc',
    #          var_name = 'avg_snlwrf',
    #          title = 'Annual means (1991–2021)',
    #          output_file_name = './output/lab1/surface-long-annual-mean.png',
    #          operator=lambda x : -1.0 * x)
    
    # # Long wave at surface plot
    # plot_map(file_name = './data/lab/net-short-annual-mean.nc',
    #          var_name = 'avg_snswrf',
    #          title = 'Annual means (1991–2021)',
    #          output_file_name = './output/lab1/surface-short-annual-mean.png')

    # Insolation map
    plot_contourf(file_name='./data/lab/tisr_month-ymonmean-zonmean.nc',
                  var_name = 'tisr',
                  title = 'Mean daily insolation',
                  output_file_name = './output/lab1/insolation.png',
                  unit = 'W * m**-2',
                  levels = 25,
                  xlabel = 'Month', ylabel = 'Latitude [deg N]',
                  operator = lambda x : (x / (3600 * 24)) [:, :, 0]) # convert J to watt and take first two indexes (time, latitude) only