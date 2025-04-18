import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import numpy as np
from matplotlib.colors import BoundaryNorm
from matplotlib.patches import FancyArrow

plt.rcParams.update({'font.size': 22})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# 添加比例尺函数
def add_scalebar(ax, lon0, lat0, length, linewidth=2, fontsize=18):
    ax.hlines(y=lat0, xmin=lon0, xmax=lon0 + length / 111, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0 + length / 111, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.text(lon0 + (length / 111) / 2, lat0 + 0.2, f"{length} km", horizontalalignment='center', fontsize=fontsize)

# 添加指北针函数
def add_north_arrow(ax, lon, lat, length=1.0, width=0.2, head_width=0.4, head_length=0.4, fontsize=18):
    ax.add_patch(FancyArrow(
        lon, lat, 0, length,  # 起点 (lon, lat) 和箭头方向 (0, length)
        width=width, head_width=head_width, head_length=head_length, color='black'
    ))
    ax.text(lon, lat + length + 1, 'N', ha='center', va='center', fontsize=fontsize, color='black')

# 加载中国边界 shapefile
china_boundary = cfeature.ShapelyFeature(
    Reader(r'D:\A-Projects\DWAA Project\Shapefile\Northern China SubRegion.shp').geometries(),
    ccrs.PlateCarree(),
    edgecolor='black',
    facecolor='none'
)

# 数据路径
base_dir = r'D:\A-Projects\DWAA Project\DWAA_Events'
location_file = r'D:\A-Projects\DWAA Project\total_dwaa_counts.csv'
stations_df = pd.read_csv(location_file)

# 初始化结果列表
results = []
for station_id in os.listdir(base_dir):
    station_folder = os.path.join(base_dir, station_id)
    if os.path.isdir(station_folder):
        dtw_file = os.path.join(station_folder, 'dry_to_wet_events.csv')
        wtd_file = os.path.join(station_folder, 'wet_to_dry_events.csv')
        
        # 初始化均值为0
        dtw_avg_IA = dtw_avg_IU = 0
        wtd_avg_IA = wtd_avg_IU = 0

        # 检查文件并计算均值
        if os.path.exists(dtw_file):
            dtw_df = pd.read_csv(dtw_file)
            if not dtw_df.empty:
                dtw_avg_IA = dtw_df['IA'].mean()
                dtw_avg_IU = dtw_df['IU'].mean()
        if os.path.exists(wtd_file):
            wtd_df = pd.read_csv(wtd_file)
            if not wtd_df.empty:
                wtd_avg_IA = wtd_df['IA'].mean()
                wtd_avg_IU = wtd_df['IU'].mean()
            
        results.append({
            'station_id': int(station_id),
            'dtw_avg_IA': 2 * dtw_avg_IA,
            'dtw_avg_IU': 2 * dtw_avg_IU,
            'wtd_avg_IA': abs(wtd_avg_IA),  # 取绝对值
            'wtd_avg_IU': abs(wtd_avg_IU)   # 取绝对值
        })

# 转换为 DataFrame 并合并经纬度
results_df = pd.DataFrame(results)
merged_df = results_df.merge(stations_df, left_on='station_id', right_on='StationID')
gdf = gpd.GeoDataFrame(merged_df, geometry=gpd.points_from_xy(merged_df['Longitude'], merged_df['Latitude']))

# 确定干湿转换事件的最大值
dry_to_wet_max = max(results_df['dtw_avg_IA'].max(), results_df['wtd_avg_IA'].max())
wet_to_dry_max = max(results_df['dtw_avg_IU'].max(), results_df['wtd_avg_IU'].max())

# 设置自定义的分类间隔
boundaries_IA = [0, 4, 8, 16, dry_to_wet_max]  # 使用相同的分类间隔
boundaries_IU = [0, 2, 4, 8, wet_to_dry_max]  # 使用相同的分类间隔
plot_labels = ['a', 'b', 'c', 'd']
# 设置颜色映射的范围
norm_IA = BoundaryNorm(boundaries_IA, ncolors=256)
norm_IU = BoundaryNorm(boundaries_IU, ncolors=256)

# 点大小设置
point_size = 12  # 调整点的大小（可以根据需要设置）

# 创建 2x2 图，右侧预留空间放图例
fig = plt.figure(figsize=(16, 9))

# 创建子图
ax1 = fig.add_subplot(2, 2, 1, projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(2, 2, 2, projection=ccrs.PlateCarree())
ax3 = fig.add_subplot(2, 2, 3, projection=ccrs.PlateCarree())
ax4 = fig.add_subplot(2, 2, 4, projection=ccrs.PlateCarree())

# 绘制地图函数
def plot_map_with_points(ax, column, cmap, norm, title, plot_idx):
    plot_labels = ['a', 'b', 'c', 'd']
    gdf.plot(column=column, cmap=cmap, markersize=point_size, ax=ax, legend=False, norm=norm, transform=ccrs.PlateCarree())
    ax.set_title(title, fontsize=22)
    ax.add_feature(china_boundary, linewidth=0.5)
    ax.set_extent([72, 136, 30, 55])
    ax.set_xticks(range(75, 140, 10), crs=ccrs.PlateCarree())
    ax.set_yticks(range(30, 55, 5), crs=ccrs.PlateCarree())
    ax.tick_params(axis='both', labelsize=18, direction='in', length=5)
    add_scalebar(ax, lon0=73, lat0=31, length=500, linewidth=2, fontsize=16)
    add_north_arrow(ax, lon=130, lat=52, length=2.0, fontsize=16)
    ax.text(0.02, 0.98, plot_labels[plot_idx], transform=ax.transAxes,
            fontsize=24, fontweight='bold', va='top', ha='left')

# 绘制四幅图
plot_map_with_points(ax1, 'dtw_avg_IA', plt.get_cmap('YlOrRd'), norm_IA, 'DTW',0)
plot_map_with_points(ax2, 'wtd_avg_IA', plt.get_cmap('YlOrRd'), norm_IA, 'WTD',1)
plot_map_with_points(ax3, 'dtw_avg_IU', plt.get_cmap('Blues'), norm_IU, 'DTW',2)
plot_map_with_points(ax4, 'wtd_avg_IU', plt.get_cmap('Blues'), norm_IU, 'WTD',3)

# 添加 IA 图例到右侧
sm_IA = plt.cm.ScalarMappable(cmap=plt.get_cmap('YlOrRd'), norm=norm_IA)
sm_IA.set_array([])

# 手动设置 IA 图例的 ticks 和 labels
cbar_IA = fig.colorbar(sm_IA, ax=[ax1, ax2], orientation='vertical', fraction=0.02, pad=0.05, ticks=boundaries_IA, label='IA', location='right')

# 添加 IU 图例到右侧
sm_IU = plt.cm.ScalarMappable(cmap=plt.get_cmap('Blues'), norm=norm_IU)
sm_IU.set_array([])

# 手动设置 IU 图例的 ticks 和 labels
cbar_IU = fig.colorbar(sm_IU, ax=[ax3, ax4], orientation='vertical', fraction=0.02, pad=0.05, ticks=boundaries_IU, label='IU', location='right')

# 调整布局，预留右侧空间给图例
plt.subplots_adjust(left=0.02, right=0.85, top=0.95, bottom=0.05, wspace=0.05, hspace=0)

# 保存图像
output_path = r'D:\A-Projects\DWAA Project\Figure\DWAA_IAIU.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')

plt.show()