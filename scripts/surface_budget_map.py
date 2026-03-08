import numpy as np
from plot_module import plot_map

if __name__ == '__main__':


    # plot_map(file_name = r'/home/nathasya/Documents/diploma_esm/data/lab/surface_budget/ssr_timmean.nc',
    #          squeeze='valid_time',
    #          var_name = 'ssr',
    #          xvar='longitude', yvar='latitude',
    #          title = 'Surface, ERA5, Annual means (1991–2020)',
    #          output_file_name = './output/surface_budget/net_radiation.png',
    #          levels=np.linspace(25, 275, 10),
    #          extend='both',
    #          operator = lambda x : (x / (3600 * 24)),
    #          cbar_label='Surface net solar radiation (W m**-2)')

    file_name = r'./data/lab/surface_budget/surface_budget_timmean_complete.nc'

    plot_map(file_name = file_name,
             squeeze='valid_time',
             var_name = 'rs',
             xvar='longitude', yvar='latitude', levels=np.linspace(25,275,10),
             title = 'Surface, ERA5, Annual means (1991–2020)',
             output_file_name = './output/surface_budget/net_radiation.png',
             cbar_label='Surface net radiation (Rs) (W m**-2)')
    
    plot_map(file_name = file_name,
             squeeze='valid_time',
             var_name = 'gs', cmap='coolwarm',
             xvar='longitude', yvar='latitude', levels=np.linspace(-200,200,10),
             title = 'Surface, ERA5, Annual means (1991–2020)',
             output_file_name = './output/surface_budget/heat_storage.png',
             cbar_label='Surface heat storage (W m**-2)')

    plot_map(file_name = file_name,
             squeeze='valid_time',
             var_name = 'avg_ishf',
             xvar='longitude', yvar='latitude', levels=np.linspace(-60,100,10),
             cmap='coolwarm',
             title = 'Surface, ERA5, Annual means (1991–2020)',
             output_file_name = './output/surface_budget/sensible_heat.png',
             operator=lambda x : -1.0 * x)
    
    plot_map(file_name = file_name,
             squeeze='valid_time',
             var_name = 'avg_slhtf',
             xvar='longitude', yvar='latitude', levels=np.linspace(0,225,10),
             title = 'Surface, ERA5, Annual means (1991–2020)',
             output_file_name = './output/surface_budget/latent_heat.png',
             operator=lambda x : -1.0 * x)