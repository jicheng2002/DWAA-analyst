# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import LogNorm
import numpy as np
from cartopy.io.shapereader import Reader
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import FancyArrow
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# 添加比例尺函数
def add_scalebar(ax, lon0, lat0, length, linewidth=2, fontsize=16):
    ax.hlines(y=lat0, xmin=lon0, xmax=lon0 + length / 111, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0 + length / 111, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.text(lon0 + (length / 111) / 2, lat0 + 0.2, f"{length} km", horizontalalignment='center', fontsize=fontsize)

# 添加指北针函数
def add_north_arrow(ax, lon, lat, length=1.0, width=0.2, head_width=0.4, head_length=0.4, fontsize=16):
    ax.add_patch(FancyArrow(
        lon, lat, 0, length,  # 起点 (lon, lat) 和箭头方向 (0, length)
        width=width, head_width=head_width, head_length=head_length, color='black'
    ))
    ax.text(lon, lat + length + 1, 'N', ha='center', va='center', fontsize=fontsize, color='black')

# Read total DWAA data
total_dwaa_df = pd.read_csv(r'D:\A-Projects\DWAA Project\total_dwaa_counts.csv')

# Retrieve station IDs, latitude, longitude, and counts for dry-to-wet and wet-to-dry events
station_ids = total_dwaa_df["StationID"].values
lats = total_dwaa_df["Latitude"].values
lons = total_dwaa_df["Longitude"].values
dry_to_wet_counts = total_dwaa_df["Dry_To_Wet_Count"].replace(0, 0.1).values
wet_to_dry_counts = total_dwaa_df["Wet_To_Dry_Count"].replace(0, 0.1).values

# 中国北方边界 shapefile
china_boundary = cfeature.ShapelyFeature(
    Reader(r'D:\A-Projects\DWAA Project\Shapefile\Northern China SubRegion.shp').geometries(),
    ccrs.PlateCarree(),
    edgecolor='black',  # Set the color of the boundary lines
    linewidth=1,
    facecolor="#FFFFFF"  # Adjust the line width as needed
)

# Set point size
point_size = 9

# 创建比较图
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10, 6))
ax.add_feature(china_boundary)
ax.set_extent([72, 136, 30, 53])

# 添加比例尺和指北针
add_scalebar(ax, lon0=73, lat0=31, length=500, linewidth=2, fontsize=16)
add_north_arrow(ax, lon=130, lat=52, length=2.0, fontsize=16)

# 添加经纬度刻度
ax.set_xticks(range(75, 140, 10), crs=ccrs.PlateCarree())  # 经度刻度
ax.set_yticks(range(30, 55, 5), crs=ccrs.PlateCarree())    # 纬度刻度
ax.tick_params(axis='both', labelsize=14, direction='in', length=5)  # 调整刻度方向和长度

# Determine color for each station based on which event count is higher
colors = np.where(dry_to_wet_counts > wet_to_dry_counts, '#E96830', '#368FE8')
# Plot comparison with conditional coloring
comparison_scatter = ax.scatter(lons, lats, color=colors, s=point_size, transform=ccrs.PlateCarree())

# 添加标题和图例
red_patch = plt.Line2D([0], [0], marker='o', color='#E96830', markerfacecolor='#E96830', markersize=8, label='Dry to Wet > Wet to Dry')
blue_patch = plt.Line2D([0], [0], marker='o', color='#368FE8', markerfacecolor='#368FE8', markersize=8, label='Wet to Dry > Dry to Wet')
plt.legend(handles=[red_patch, blue_patch], loc='upper center')  # 将图例放在左下角
plt.rcParams.update({'font.size': 18})
# 调整布局和保存图片
plt.tight_layout()
output_path = r'D:\A-Projects\DWAA Project\Figure\Compare_DTW_WTD_with_map_features.png'
plt.savefig(output_path, dpi=300)

# 显示图片
plt.show()

