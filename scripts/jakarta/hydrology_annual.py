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

    # Read data
    ds_e = xr.open_dataset('./data/lab/surface_budget/e_ymonmean.nc')
    ds_pev = xr.open_dataset('./data/lab/surface_budget/pev_ymonmean.nc')
    ds_tp = xr.open_dataset('./data/lab/surface_budget/tp_ymonmean.nc')
    ds_t2m = xr.open_dataset('./data/lab/surface_budget/t2m_ymonmean.nc')

    # Subset
    ds_e = representative_cell(ds_e, lon, lat)
    ds_pev = representative_cell(ds_pev, lon, lat)
    ds_tp = representative_cell(ds_tp, lon, lat)
    ds_t2m = representative_cell(ds_t2m, lon, lat)

    # Convert unit
    ds_tp['tp'] = ds_tp['tp'] * 1e3 # m to mm
    ds_e['e'] = ds_e['e'] * -1e3 # m to mm, evapotranspiration to be positive
    ds_pev['pev'] = ds_pev['pev'] * -1e3 # m to mm
    ds_t2m['t2m'] = ds_t2m['t2m'] - 273.15 # k to deg c

    # Initialize figure
    fig, ax = plt.subplots(figsize=(12,6))

    # Plot data
    ax.plot(ds_tp['tp'], 'b--', label='P')
    ax.plot(ds_e['e'], 'r--', label='E')
    ax.plot(ds_pev['pev'], 'k', label='PET')

     # Create second y-axis for temperature
    ax2 = ax.twinx()
    ax2.plot(ds_t2m['t2m'], color='darkred', linewidth=2.5, marker='o', label='Temperature (°C)')

    # Month labels
    month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"]
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_labels)

    # Axis labels
    ax.set_xlabel('month')
    ax.set_ylabel('mm/day')
    ax2.set_ylabel('Surface temperature (°C)', color='darkred')
    ax.legend(loc='upper right'); ax2.legend(loc='lower right')

    #Title
    plt.title('Hydrological Cycle - Jakarta')
    plt.savefig('./output/hydrology/annual_cycle_jkt.png')
