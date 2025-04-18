import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.patches import FancyArrow

# Set font styles
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# Paths
base_dir_decades = r'D:\A-Projects\DWAA Project\DWAA_Decades_Stations'
base_dir_seasons = r'D:\A-Projects\DWAA Project\DWAA_Seasons_Stations'
output_path = r'D:\A-Projects\DWAA Project\Figure'

# Define time periods and plot labels
time_periods = [(1980, 1990), (1990, 2000), (2000, 2010), (2010, 2020)]
seasons = ["Spring", "Summer", "Autumn", "Winter"]
plot_labels1 = ['a', 'b', 'c', 'd']
plot_labels2 = ['e', 'f', 'g', 'h']

# Define bins, labels, and custom colors for the legend
bins = [-9999, 0, 1, 2, 3, 4, np.inf]  
labels = ['0', '1', '2', '3', '4', '>4']

colors = ['#d9d9d9', '#a6d96a', '#66bd63', '#1a9850', '#006837', '#00441b']
color1 = ['#B7B7B7', '#398FDA', '#FFD074', '#FF8000', '#CB947C', '#CC0000']
color2 = ['#C9C8C7', '#CCFFCC', '#66FFB2', '#66B2FF', '#0066CC', '#003366']

cmap = ListedColormap(colors)
cmap1 = ListedColormap(color1)
cmap2 = ListedColormap(color2)
# Load China boundary shapefile
china_boundary = cfeature.ShapelyFeature(
    Reader(r'D:\A-Projects\DWAA Project\Shapefile\Northern China SubRegion.shp').geometries(),
    ccrs.PlateCarree(),
    edgecolor='black',
    linewidth=0.5,
    facecolor='none'
)

# Function: Add a scale bar
def add_scalebar(ax, lon0, lat0, length, linewidth=2, fontsize=16):
    ax.hlines(y=lat0, xmin=lon0, xmax=lon0 + length / 111, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0 + length / 111, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.text(lon0 + (length / 111) / 2, lat0 + 0.2, f"{length} km", horizontalalignment='center', fontsize=fontsize)

# Function: Add a north arrow
def add_north_arrow(ax, lon, lat, length=1.0, width=0.2, head_width=0.4, head_length=0.4, fontsize=16):
    ax.add_patch(FancyArrow(
        lon, lat, 0, length,  # Start point (lon, lat) and arrow direction (0, length)
        width=width, head_width=head_width, head_length=head_length, color='black'
    ))
    ax.text(lon, lat + length + 1, 'N', ha='center', va='center', fontsize=fontsize, color='black')

# Function: Enhance map with features
def enhance_map(ax):
    ax.add_feature(china_boundary, linewidth=0.5)  # Add China boundary
    ax.set_extent([72, 136, 30, 53])  # Set map extent
    ax.set_xticks(range(75, 140, 10), crs=ccrs.PlateCarree())  # Add longitude ticks
    ax.set_yticks(range(30, 55, 5), crs=ccrs.PlateCarree())    # Add latitude ticks
    ax.tick_params(axis='both', labelsize=16, direction='in', length=5)  # Adjust tick attributes
    add_scalebar(ax, lon0=73, lat0=31, length=500, linewidth=2, fontsize=16)  # Add scale bar
    add_north_arrow(ax, lon=130, lat=52, length=2.0, fontsize=16)  # Add north arrow

# Function: Load data for decades or seasons
def load_data(base_dir, event_types):
    data_frames = {}
    for file_name in os.listdir(base_dir):
        if any(event_type in file_name for event_type in event_types) and file_name.endswith('.csv'):
            # Extract the period and event type
            for event_type in event_types:
                if event_type in file_name:
                    period_key = file_name.replace(event_type + '_', '').replace('.csv', '')
                    df = pd.read_csv(os.path.join(base_dir, file_name))
                    if period_key not in data_frames:
                        data_frames[period_key] = {}
                    data_frames[period_key][event_type] = df
    return data_frames


# Define event types
event_types = ['dry_to_wet', 'wet_to_dry']

# Load data for decades and seasons
decades_data = load_data(base_dir_decades, event_types)
seasons_data = load_data(base_dir_seasons, event_types)


# ------------------- Plot for Time Period Dry-to-Wet (DTW) Events -------------------
fig, axs = plt.subplots(2, 2, figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})

for i, period in enumerate(time_periods):
    start_year, end_year = period
    period_key = f'{start_year}_{end_year}'
    
    # Access the specific event type (e.g., 'dry_to_wet')
    if period_key not in decades_data or 'dry_to_wet' not in decades_data[period_key]:
        print(f"Data for dry_to_wet in period {period_key} is missing.")
        continue

    df = decades_data[period_key]['dry_to_wet']  # Access the 'wet_to_dry' DataFrame
    print(f"Type of df for period {period_key}: {type(df)}")
    print(f"Columns in df: {df.columns}")

    if not {'Latitude', 'Longitude', 'Count'}.issubset(df.columns):
        print(f"Missing required columns in period {period_key}.")
        continue

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
    gdf['Bins'] = pd.cut(gdf['Count'], bins=bins, labels=labels, include_lowest=True)

    ax = axs[i // 2, i % 2]
    enhance_map(ax)
    gdf.plot(
        column='Bins', cmap=cmap1, markersize=9,
        ax=ax, legend=False, transform=ccrs.PlateCarree()
    )
    ax.set_title(f'DTW {start_year}-{end_year}')
    
    legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
    for color, label in zip(color1, labels)
    ]
        # Add the legend to the axis
    ax.legend(
        handles=legend_elements, loc='upper center', fontsize=16,
        title='Frequency', frameon=False, ncol=2
    )
    ax.text(0.02, 0.98, plot_labels1[i], transform=ax.transAxes,
            fontsize=22, fontweight='bold', va='top', ha='left')

plt.tight_layout(rect=[0, 0.01, 1, 1])  # Adjust layout
plt.savefig(os.path.join(output_path, "DTW_Time_Periods.png"), dpi=300)

# ------------------- Plot for Seasonal Dry-to-Wet (DTW) Events -------------------
fig, axs = plt.subplots(2, 2, figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})

for i, season in enumerate(seasons):
    if season in seasons_data:
        df = seasons_data[season]['dry_to_wet']
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
        gdf['Bins'] = pd.cut(gdf['Count'], bins=bins, labels=labels, include_lowest=True)
        ax = axs[i // 2, i % 2]
        enhance_map(ax)
        gdf.plot(
            column='Bins', cmap=cmap1, markersize=9,
            ax=ax, legend=False, transform=ccrs.PlateCarree()
        )
        ax.set_title(f'DTW {season}')

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
            for color, label in zip(color1, labels)
            ]
        # Add the legend to the axis
        ax.legend(
            handles=legend_elements, loc='upper center', fontsize=16,
            title='Frequency', frameon=False, ncol=2
            )
        ax.text(0.02, 0.98, plot_labels1[i], transform=ax.transAxes,
            fontsize=22, fontweight='bold', va='top', ha='left')
plt.tight_layout(rect=[0, 0.01, 1, 1])  # Adjust layout
plt.savefig(os.path.join(output_path, "DTW_Season.png"), dpi=300)
  
# ------------------- Plot for Time Period Dry-to-Wet (DTW) Events -------------------
fig, axs = plt.subplots(2, 2, figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})

for i, period in enumerate(time_periods):
    start_year, end_year = period
    period_key = f'{start_year}_{end_year}'
    
    # Access the specific event type (e.g., 'dry_to_wet')
    if period_key not in decades_data or 'wet_to_dry' not in decades_data[period_key]:
        print(f"Data for wet_to_dry in period {period_key} is missing.")
        continue

    df = decades_data[period_key]['wet_to_dry']  # Access the 'wet_to_dry' DataFrame
    print(f"Type of df for period {period_key}: {type(df)}")
    print(f"Columns in df: {df.columns}")

    if not {'Latitude', 'Longitude', 'Count'}.issubset(df.columns):
        print(f"Missing required columns in period {period_key}.")
        continue

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
    gdf['Bins'] = pd.cut(gdf['Count'], bins=bins, labels=labels, include_lowest=True)

    ax = axs[i // 2, i % 2]
    enhance_map(ax)
    gdf.plot(
        column='Bins', cmap=cmap2, markersize=9,
        ax=ax, legend=False, transform=ccrs.PlateCarree()
    )
    ax.set_title(f'WTD {start_year}-{end_year}')
    legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
    for color, label in zip(color2, labels)
    ]
        # Add the legend to the axis
    ax.legend(
        handles=legend_elements, loc='upper center', fontsize=16,
        title='Frequency', frameon=False, ncol=2
    )
    ax.text(0.02, 0.98, plot_labels2[i], transform=ax.transAxes,
            fontsize=22, fontweight='bold', va='top', ha='left')
# Save the figure
plt.tight_layout(rect=[0, 0.01, 1, 1])  # Adjust layout
plt.savefig(os.path.join(output_path, "WTD_Time_Periods.png"), dpi=300)


# ------------------- Plot for Seasonal Wet-to-Dry (WTD) Events -------------------
fig, axs = plt.subplots(2, 2, figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})

for i, season in enumerate(seasons):
    if season in seasons_data:
        df = seasons_data[season]['wet_to_dry'] 
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
        gdf['Bins'] = pd.cut(gdf['Count'], bins=bins, labels=labels, include_lowest=True)
        ax = axs[i // 2, i % 2]
        enhance_map(ax)
        gdf.plot(
            column='Bins', cmap=cmap2, markersize=9,
            ax=ax, legend=False, transform=ccrs.PlateCarree()
        )
        ax.set_title(f'WTD {season}')
        # Add legend within each subplot
        legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
    for color, label in zip(color2, labels)
    ]
        # Add the legend to the axis
    ax.legend(
        handles=legend_elements, loc='upper center', fontsize=16,
        title='Frequency', frameon=False, ncol=2
    )
    ax.text(0.02, 0.98, plot_labels2[i], transform=ax.transAxes,
            fontsize=22, fontweight='bold', va='top', ha='left')

plt.tight_layout(rect=[0, 0.01, 1, 1])  # Adjust layout
plt.savefig(os.path.join(output_path, "WTD_Seasons.png"), dpi=300)

plt.show()

