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
    ds_ro = xr.open_dataset('./data/lab/surface_budget/ro_ymonmean.nc')
    ds_m = xr.open_dataset('./data/lab/surface_budget/swvl1_ymonmean.nc')
    ds_tcc = xr.open_dataset('./data/lab/surface_budget/tcc_ymonmean.nc')

    # Subset
    ds_e = representative_cell(ds_e, lon, lat)
    ds_pev = representative_cell(ds_pev, lon, lat)
    ds_tp = representative_cell(ds_tp, lon, lat)
    ds_t2m = representative_cell(ds_t2m, lon, lat)
    ds_ro = representative_cell(ds_ro, lon, lat)
    ds_m = representative_cell(ds_m, lon, lat)
    ds_tcc = representative_cell(ds_tcc, lon, lat)

    # Convert unit
    ds_tp['tp'] = ds_tp['tp'] * 1e3 # m to mm
    ds_e['e'] = ds_e['e'] * -1e3 # m to mm, evapotranspiration to be positive
    ds_pev['pev'] = ds_pev['pev'] * -1e3 # m to mm
    ds_t2m['t2m'] = ds_t2m['t2m'] - 273.15 # k to deg c
    ds_ro['ro'] *= 1e3

    # Sum all ds_m

    # Initialize figure
    fig, (ax, ax_bottom) = plt.subplots(
    2, 1, figsize=(12, 10), sharex=True,
    gridspec_kw={'height_ratios': [2, 1]}
    )

    # Plot data
    ax.plot(ds_tp['tp'], 'b--', label='P')
    ax.plot(ds_e['e'], 'r--', label='E')
    ax.plot(ds_pev['pev'], 'k', label='PET')
    ax.plot(ds_ro['ro'], '--', color='gray', label='ΔF')

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

    # -------------------------
    # BOTTOM PLOT
    ax_bottom.plot(ds_m['swvl1'], color='purple', label='Surface moisture')
    ax_bottom.plot(ds_tcc['tcc'], color='gray', label='Total cloud cover')

    ax_bottom.set_ylabel('unitless')
    ax_bottom.set_ylim(0, 1)
    ax_bottom.set_xlabel('month')
    ax_bottom.legend()

    #Title
    plt.title('Hydrological Cycle - Jakarta')
    plt.savefig('./output/hydrology/annual_cycle_jkt.png')
