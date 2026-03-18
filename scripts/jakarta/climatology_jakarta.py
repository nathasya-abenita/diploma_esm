import xarray as xr
import matplotlib.pyplot as plt
from module import representative_cell

if __name__ == '__main__':
    # Jakarta bounds
    bounds = dict(
        lon_min=106.67,
        lon_max=106.97,
        lat_min=-6.09,
        lat_max=-6.35
    )
    lon, lat = (106.8229, -6.1944) # jakarta center

    # Define data location
    file_name_tp = r'./data/lab/surface_budget/tp_ymonmean.nc'
    file_name_t2m = r'./data/lab/surface_budget/t2m_ymonmean.nc'

    # Read data
    ds_tp = xr.open_dataset(file_name_tp)
    ds_t2m = xr.open_dataset(file_name_t2m)

    # Subset
    ds_tp = representative_cell(ds_tp, lon, lat)
    ds_t2m = representative_cell(ds_t2m, lon, lat)

    # Initialize figure
    fig, ax = plt.subplots(figsize=(12,6))

    # Extract data
    precip = ds_tp['tp'] * 1e3 # m to mm
    temp = ds_t2m['t2m'] - 273.15 # k to deg c

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
    plt.title("Monthly Climatology - Jakarta")

    # Save plot
    plt.savefig('./output/climatology_jkt.png', dpi=300, bbox_inches='tight')