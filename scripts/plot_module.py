"""
Author: Nathasya Christien
Starting Date: 2026-02-22
Description: All about plottings with xarray!
""" 

#%% Import packages
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import cartopy.crs as ccrs 
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

#%% Plotting functions

def plot_line_budget(file_name1, file_name2, var_name1, var_name2, title,
                     output_file_name, operator1=None, operator2=None):
    """ Budget is defined as data1 - data2 """
    """TODO: Generalize the plotting labels and legends"""
    
    # Read data
    ds1, ds2 = xr.open_dataset(file_name1), xr.open_dataset(file_name2)

    # Apply operators
    if operator1 != None:
        ds1[var_name1] = operator1(ds1[var_name1])
    if operator2 != None:
        ds2[var_name2] = operator2(ds2[var_name2])

    # Initialize figure
    fig, axs = plt.subplots(2, 1, figsize = (10, 6), sharex=True)
    
    # Plot short-wave and long-wave
    ds1[var_name1].plot(ax=axs[0], label=ds1[var_name1].attrs['long_name'], color='tab:orange')
    ds2[var_name2].plot(ax=axs[0], label=ds2[var_name2].attrs['long_name'], color='tab:blue')
    axs[0].set_ylabel(f'Radiation ({ds1[var_name1].attrs['units']})')
    axs[0].set_xlabel('')
    axs[0].set_title(''); axs[0].grid()
    axs[0].legend()

    # Plot budget
    net = ds1[var_name1] - ds2[var_name2]
    net.plot(ax=axs[1], color='tab:green', label='Net radiation flux')
    axs[1].legend()
    axs[1].set_ylabel(f'Radiation ({ds1[var_name1].attrs['units']})')
    axs[1].set_xlabel('Latitude [deg N]')
    axs[1].set_title(''); axs[1].grid(); axs[1].set_xlim(-90, 90)

    # Add title
    plt.suptitle(title)

    # Save picture
    plt.tight_layout()
    plt.savefig(output_file_name)

def plot_line (file_name, var_name, title, output_file_name):
    # Read data
    ds = xr.open_dataset(file_name)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ds[var_name].plot(ax=ax)

    # Check if the x-axis coordinate is datetime-like, then take months only
    xcoord = ds[var_name].coords['valid_time'] 
    if np.issubdtype(xcoord.dtype, np.datetime64): 
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())

    # Activate grid and set tite
    plt.grid(); ax.set_title(title)

    # Save picture
    plt.savefig(output_file_name)

def plot_contour (file_name, var_name, title, output_file_name, xvar, yvar, xlabel=None, ylabel=None, operator=None, north=None):
    # Read data
    ds = xr.open_dataset(file_name)
    
    # Apply operation to variable if needed
    if operator != None:
        ds[var_name] = operator(ds[var_name])

    # Create figure with Cartopy projection 
    fig = plt.figure(figsize=(12, 6)) 
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

    # Select hemisphere
    if north != None:
        if north:
            ax.set_ylim(0, 90)
        else:
            ax.set_ylim(-90, 0)

    # Variable name label
    cbar_label = rf"{ds[var_name].attrs['long_name']} ({ds[var_name].attrs['units']})"

    # Plot
    contours = xr.plot.contour(ds[var_name],
                ax=ax,
                transform=ccrs.PlateCarree(),
                x=xvar, y=yvar, levels=7, linewidth=0.6,
                cmap='rainbow')
    ax.clabel(contours, inline=True, fontsize=10)
    ax.set_title(cbar_label)
    plt.suptitle(title)

    # Save picture
    ax.coastlines() 
    ax.add_feature(cfeature.BORDERS, linewidth=0.5) 
    plt.savefig(output_file_name)

def plot_contourf_nonmap (file_name, var_name, title, output_file_name, xvar, yvar, levels=10, 
                          squeeze=None, xlabel=None, ylabel=None, unit=None, operator=None):
    # Read data
    ds = xr.open_dataset(file_name)
    if squeeze != None:
        ds = ds.squeeze(squeeze)
    
    # Apply operation to variable if needed
    if operator != None:
        ds[var_name] = operator(ds[var_name])

    # Color bar label
    if unit == None:
        cbar_label = rf"{ds[var_name].attrs['long_name']} ({ds[var_name].attrs['units']})"
    else:
        cbar_label = rf"{ds[var_name].attrs['long_name']} ({unit})"

    # Build a discrete version of a colormap
    base = plt.get_cmap('turbo') 
    colors = base(np.linspace(0, 1, levels)) 
    # Find the index corresponding to value 0 
    vmin = ds[var_name].min(); vmax = ds[var_name].max() 
    zero_pos = int((0 - vmin) / (vmax - vmin) * (levels - 1)) 
    # Set that color to white 
    colors[zero_pos] = np.array([1, 1, 1, 1]) 
    # Create new colormap 
    new_cmap = mcolors.ListedColormap(colors)

    # Initialize figure
    fig, ax = plt.subplots(figsize=(10, 6)) 

    # Plot
    xr.plot.contourf(ds[var_name], x=xvar, y=yvar, cbar_kwargs={'label': cbar_label}, cmap=new_cmap, levels=levels)
    ax.set_title(title)

    # Check if the x-axis coordinate is datetime-like, then take months only
    if 'valid_time' in list(ds[var_name].coords):
        xcoord = ds[var_name].coords['valid_time'] 
        if np.issubdtype(xcoord.dtype, np.datetime64): 
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # Add border
    if xvar == 'longitude':
        ax.coastlines() 
        ax.add_feature(cfeature.BORDERS, linewidth=0.5) 

    # Set labels
    if xlabel != None:
        ax.set_xlabel(xlabel)
    if ylabel != None:
        ax.set_ylabel(ylabel)

    # Save picture
    plt.savefig(output_file_name)

def plot_map (file_name, var_name, title, output_file_name, xvar, yvar, levels=10, 
              squeeze=None,operator=None, north=None, mollweide=True, cmap='turbo', extend=None):
    # Read data 
    ds = xr.open_dataset(file_name)
    if squeeze != None:
        ds = ds.squeeze(squeeze)
    
    # Apply operation to variable if needed
    if operator != None:
        ds[var_name] = operator(ds[var_name])

    # Create figure with Cartopy projection 
    fig = plt.figure(figsize=(10, 6)) 
    if mollweide:
        ax = plt.axes(projection=ccrs.Mollweide(central_longitude=180))
    else:
        ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

    # Select hemisphere
    if north != None:
        if north:
            # Set extent: [west, east, south, north] in PlateCarree coordinates 
            ax.set_extent([-180, 180, 0, 90], crs=ccrs.PlateCarree())
        else:
            ax.set_extent([-180, 180, -90, 0], crs=ccrs.PlateCarree())

    # Color bar label
    cbar_label = rf"{ds[var_name].attrs['long_name']} ({ds[var_name].attrs['units']})"

    # Plot variable
    cf = xr.plot.contourf(ds[var_name], ax=ax, x=xvar, y=yvar, transform=ccrs.PlateCarree(),
                     cbar_kwargs={'label': cbar_label, 'orientation': 'horizontal', 'pad': 0.05}, 
                     cmap=cmap, levels=levels, extend=extend)
    
    # Edit colorbar by rounding
    # cbar = cf.colorbar
    # cbar.formatter = mticker.FormatStrFormatter('%.0f') 
    # cbar.update_ticks()
    # Add borders
    ax.coastlines() 
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    # Add grid
    activate_geo_grid(ax)
    # Lay out
    ax.set_title(title)
    plt.tight_layout()
    # Save pricture
    plt.savefig(output_file_name)

def activate_geo_grid (ax):
    gl = ax.gridlines( draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--' ) 
    # Turn on/off labels for each side 
    gl.top_labels = False 
    gl.right_labels = False 
    # Format lon/lat labels 
    gl.xformatter = LongitudeFormatter() 
    gl.yformatter = LatitudeFormatter() 