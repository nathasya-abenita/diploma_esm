import xarray as xr
import matplotlib.pyplot as plt
from module_calculation import subset_with_regionmask, fldmean
from module_plot import plot_ds_sub_grids

if __name__ == '__main__':
    # Bounds
    # 7.354842°S 106.411503°E
    # 6.486221°S 108.514835°E
    # bounds = dict(
    #     lon_min=106.411,
    #     lon_max=108.5148,
    #     lat_min=-6.09,
    #     lat_max=-7.354
    # )
    shp_path = r'./data/spatial/west_java/west_java.shp'

    # Define data location
    file_name_tp = r'./data/lab/surface_budget/tp_ymonmean.nc'
    file_name_t2m = r'./data/lab/surface_budget/t2m_ymonmean.nc'

    # Read data
    ds_tp = xr.open_dataset(file_name_tp)
    ds_t2m = xr.open_dataset(file_name_t2m)

    # Subset
    ds_tp = subset_with_regionmask(ds_tp, shp_path)
    ds_t2m = subset_with_regionmask(ds_t2m, shp_path)

    # Plot grids
    plot_ds_sub_grids(ds_tp)

    # Compute fldmean
    da_tp = fldmean(ds_tp, 'tp')
    da_t2m = fldmean(ds_t2m, 't2m')

    # Initialize figure
    fig, ax = plt.subplots(figsize=(12,6))

    # Extract data and convert unit
    precip = da_tp.values * 1e3   # total precipitation
    temp = da_t2m.values - 273.15      # temperature

    # Plot precipitation as bars
    ax.bar(range(12), precip, color='royalblue', alpha=0.6, label='Precipitation (mm)')

    # Create second y-axis for temperature
    ax2 = ax.twinx()
    ax2.plot(range(12), temp, color='darkred', linewidth=2.5, marker='o', label='Temperature (°C)')

    # Month labels
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"]
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_labels)

    # Labels
    ax.set_ylabel('Total precipitation (mm/d)', color='royalblue')
    ax2.set_ylabel('Surface temperature (°C)', color='darkred')
    ax.set_xlabel('Month')

    # Title
    plt.title("Monthly Climatology - West Java")

    # Save plot
    plt.savefig('./output/climatology_west_java.png', dpi=300, bbox_inches='tight')
    # plt.show()

'''
    # Initialize figure
    fig, axs = plt.subplots(2, 1, figsize=(12,6), sharex=True)

    # Plot
    axs[0].plot(ds_tp['tp'].data[:, 0, 0])
    axs[1].plot(ds_t2m['t2m'].data[:, 0, 0])

    # Activate monthly index name
    month_labels = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
    ]
    axs[1].set_xticks(range(0, 12))
    axs[1].set_xticklabels(month_labels)

    # Correct labels
    axs[0].set_ylabel('Total precipitation (mm)')
    axs[1].set_ylabel('Surface temperature (deg C)')
    axs[1].set_xlabel('Month')

    # Save plot
    plt.savefig(r'./output/climatology.png')
'''