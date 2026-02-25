"""
Author: Nathasya Christien
Starting Date: 2026-02-22
Description: Plotting ERA5 and temperature data for lab #1
""" 

import numpy as np
from plot_module import plot_map, plot_contourf_nonmap, plot_line_budget, plot_line

if __name__ == '__main__':

    # # Long wave at surface plot
    # plot_map(file_name = './data/lab/net-long-annual-mean.nc',
    #          squeeze='valid_time',
    #          var_name = 'avg_snlwrf',
    #          xvar='longitude', yvar='latitude', levels=16,
    #          title = 'Surface, ERA5, Annual means (1991–2021)',
    #          output_file_name = './output/lab1/surface-long-annual-mean.png',
    #          operator=lambda x : -1.0 * x)
    
    # # Long wave at surface plot
    # plot_map(file_name = './data/lab/net-short-annual-mean.nc',
    #          squeeze='valid_time',
    #          xvar='longitude', yvar='latitude', levels=16,
    #          var_name = 'avg_snswrf',
    #          title = 'Surface, ERA5, Annual means (1991–2021)',
    #          output_file_name = './output/lab1/surface-short-annual-mean.png')

    # Long wave at TOA plot
    plot_map(file_name = './data/lab/tnlwrf-timmean.nc',
             squeeze='valid_time',
             xvar='longitude', yvar='latitude', levels=np.linspace(120, 300, 10),
             var_name = 'avg_tnlwrf',
             title = 'TOA, ERA5, Annual means (1991–2021)',
             output_file_name = './output/lab1/toa-long-annual-mean.png',
             operator=lambda x : -1.0 * x)
    
    # # Long wave at TOA plot
    # plot_map(file_name = './data/lab/tnswrf-timmean.nc',
    #          squeeze='valid_time',
    #          xvar='longitude', yvar='latitude', levels=np.linspace(40, 360, 17),
    #          var_name = 'avg_tnswrf',
    #          title = 'TOA, ERA5, Annual means (1991–2021)',
    #          output_file_name = './output/lab1/toa-short-annual-mean.png')

    # # Insolation map
    # plot_contourf_nonmap(file_name='./data/lab/tisr_month-ymonmean-zonmean.nc',
    #               var_name = 'tisr', squeeze = 'lon',
    #               xvar = 'valid_time', yvar = 'lat',
    #               title = 'Mean daily insolation',
    #               output_file_name = './output/lab1/insolation.png',
    #               unit = 'W * m**-2',
    #               levels = 25,
    #               xlabel = 'Month', ylabel = 'Latitude [deg N]',
    #               operator = lambda x : (x / (3600 * 24))) # convert J to watt

    # # Zonal mean surface long and short wave budget
    # plot_line_budget(file_name2='./data/lab/net-long-annual-zonmean.nc', var_name2='avg_snlwrf',
    #                  file_name1='./data/lab/net-short-annual-zonmean.nc', var_name1='avg_snswrf',
    #                  output_file_name='./output/lab1/surface-radiation-budget.png',
    #                  title='Surface Zonal Mean Radiation Budget',
    #                  operator2=lambda x : -1.0 * x)
    
    # # Zonal mean TOA long and short wave budget
    # plot_line_budget(file_name2='./data/lab/tnlwrf-timmean-zonmean.nc', var_name2='avg_tnlwrf',
    #                  file_name1='./data/lab/tnswrf-timmean-zonmean.nc', var_name1='avg_tnswrf',
    #                  output_file_name='./output/lab1/toa-radiation-budget.png',
    #                  title='Surface Zonal Mean Radiation Budget',
    #                  operator2=lambda x : -1.0 * x)

    # # Global surface downward short wave
    # plot_line(file_name = './data/lab/avg_sdirswrf_ymonmean_fldmean.nc', 
    #           var_name = 'avg_sdirswrf', 
    #           title = 'Global zonal mean for surface direct short-wave', 
    #           output_file_name = './output/lab1/zonmean-surface-direct-short-wave.png')

    # # Amplitude of seasonal cycle for surface temperature
    # plot_map(file_name = './data/lab/t2m_diffTemp.nc',
    #          squeeze='valid_time',
    #          xvar='longitude', yvar='latitude',
    #          mollweide=False,
    #          var_name = 't2m', north = True,
    #          title = 'Seasonal cycle amplitude for surface temperature',
    #          output_file_name ='./output/lab1/amplitude-t2m-map.png',
    #          operator=lambda x : x.where(x['latitude'] >= 0, drop=True),
    #          extend = 'both') 

    # # Average minus zonal mean temperature
    # plot_map(file_name = './data/lab/t2m-anomaly.nc',
    #          xvar='lon', yvar='lat', squeeze='valid_time',
    #          mollweide=False,
    #          var_name = 't2m',
    #          title = 'Difference between the annual mean surface temperature and the zonal mean temperature',
    #          output_file_name ='./output/lab1/t2m-anomaly.png',
    #          extend='both')

    # # Variability
    # plot_map(file_name = './data/lab/CRU-Temp_sig.nc',
    #          xvar='lon', yvar='lat', squeeze='time',
    #          mollweide=False,
    #          var_name = 'tmp',
    #          title = 'Surface temperature interannual variability (std)',
    #          output_file_name ='./output/lab1/t2m-var.png')