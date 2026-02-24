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
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def plot_line_budget(file_name1, file_name2, var_name1, var_name2, 
                     output_file_name, operator1=None, operator2=None):
    """ Budget is defined as data1 - data2 """
    
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
    ds1[var_name1].plot(ax=axs[0], label=ds1[var_name1].attrs['long_name'])
    ds2[var_name2].plot(ax=axs[0], label=ds2[var_name2].attrs['long_name'])
    axs[0].set_ylabel(f'Radiation ({ds1[var_name1].attrs['units']})')
    axs[0].set_xlabel('')
    axs[0].set_title(''); axs[0].grid()
    axs[0].legend()

    # Plot budget
    net = ds1[var_name1] - ds2[var_name2]
    net.plot(ax=axs[1])
    axs[1].set_ylabel(f'Radiation ({ds1[var_name1].attrs['units']})')
    axs[1].set_xlabel('Latitude [deg N]')
    axs[1].set_title(''); axs[1].grid()

    # Save picture
    plt.savefig(output_file_name)

def plot_line (file_name, var_name, title, output_file_name):
    # Read data
    ds = xr.open_dataset(file_name)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
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

def plot_contourf_nonmap (file_name, var_name, title, output_file_name, xvar, yvar, levels=10, xlabel=None, ylabel=None, unit=None, operator=None):
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

def plot_map (file_name, var_name, title, output_file_name, operator=None, north=None, mollweide=True):
    # Read data 
    ds = xr.open_dataset(file_name)
    
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
    p = ds[var_name].plot(ax=ax, 
                            transform=ccrs.PlateCarree(),
                            cbar_kwargs={
                                    'label': cbar_label, 
                                    'orientation': 'horizontal', 
                                    'pad': 0.05
                                        },
                            cmap='coolwarm')
    
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

if __name__ == '__main__':

    # Long wave at surface plot
    plot_map(file_name = './data/lab/net-long-annual-mean.nc',
             var_name = 'avg_snlwrf',
             title = 'Annual means (1991–2021)',
             output_file_name = './output/lab1/surface-long-annual-mean.png',
             operator=lambda x : -1.0 * x)
    
    # # Long wave at surface plot
    plot_map(file_name = './data/lab/net-short-annual-mean.nc',
             var_name = 'avg_snswrf',
             title = 'Annual means (1991–2021)',
             output_file_name = './output/lab1/surface-short-annual-mean.png')

    # Long wave at surface plot
    plot_map(file_name = './data/lab/tnlwrf-timmean.nc',
             var_name = 'avg_tnlwrf',
             title = 'Annual means (1991–2021)',
             output_file_name = './output/lab1/toa-long-annual-mean.png',
             operator=lambda x : -1.0 * x)
    
    # Long wave at surface plot
    plot_map(file_name = './data/lab/tnswrf-timmean.nc',
             var_name = 'avg_tnswrf',
             title = 'Annual means (1991–2021)',
             output_file_name = './output/lab1/toa-short-annual-mean.png')

    # Insolation map
    plot_contourf_nonmap(file_name='./data/lab/tisr_month-ymonmean-zonmean.nc',
                  var_name = 'tisr',
                  xvar = 'valid_time', yvar = 'lat',
                  title = 'Mean daily insolation',
                  output_file_name = './output/lab1/insolation.png',
                  unit = 'W * m**-2',
                  levels = 25,
                  xlabel = 'Month', ylabel = 'Latitude [deg N]',
                  operator = lambda x : (x / (3600 * 24)) [:, :, 0]) # convert J to watt and take first two indexes (time, latitude) only

    # Zonal mean surface long and short wave budget
    plot_line_budget(file_name2='./data/lab/net-long-annual-zonmean.nc', var_name2='avg_snlwrf',
                     file_name1='./data/lab/net-short-annual-zonmean.nc', var_name1='avg_snswrf',
                     output_file_name='./output/lab1/surface-radiation-budget.png',
                     operator2=lambda x : -1.0 * x)
    # Zonal mean TOA long and short wave budget
    plot_line_budget(file_name2='./data/lab/tnlwrf-timmean-zonmean.nc', var_name2='avg_tnlwrf',
                     file_name1='./data/lab/tnswrf-timmean-zonmean.nc', var_name1='avg_tnswrf',
                     output_file_name='./output/lab1/toa-radiation-budget.png',
                     operator2=lambda x : -1.0 * x)

    # Global surface downward short wave
    plot_line(file_name = './data/lab/avg_sdirswrf_ymonmean_fldmean.nc', 
              var_name = 'avg_sdirswrf', 
              title = 'Global zonal mean for surface direct short-wave', 
              output_file_name = './output/lab1/zonmean-surface-direct-short-wave.png')

    # Amplitude of seasonal cycle for surface temperature [UNUSED]
    # plot_contour (file_name='./data/lab/t2m_diffTemp.nc', 
    #               var_name='t2m', 
    #               title='Seasonal cycle amplitude for surface temperature', 
    #               output_file_name='./output/lab1/amplitude-t2m.png',
    #               xvar = 'longitude', yvar = 'latitude',
    #               north = True,
    #               operator=lambda x : x.where(x['latitude'] >= 0, drop=True) [0, :, :]) # take lat and lon only

    # Amplitude of seasonal cycle for surface temperature
    plot_map(file_name = './data/lab/t2m_diffTemp.nc',
             mollweide=False,
             var_name = 't2m', north = True,
             title = 'Seasonal cycle amplitude for surface temperature',
             output_file_name ='./output/lab1/amplitude-t2m-map.png',
             operator=lambda x : x.where(x['latitude'] >= 0, drop=True) [0, :, :]) # take lat and lon only

    # Average minus zonal mean temperature
    plot_map(file_name = './data/lab/t2m-anomaly.nc',
             mollweide=False,
             var_name = 't2m',
             title = 'Difference between the annual mean surface temperature and the zonal mean temperature',
             output_file_name ='./output/lab1/t2m-anomaly.png') # take lat and lon only

    # Variability
    plot_map(file_name = './data/lab/CRU-Temp_sig.nc',
             mollweide=True,
             var_name = 'tmp',
             title = 'Surface temperature variability (std)',
             output_file_name ='./output/lab1/t2m-var.png')