# 导入必要的库
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
import numpy as np
from matplotlib.patches import FancyArrow
plt.rcParams.update({'font.size': 22})
plt.rcParams.update({'font.size': 22})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# 函数：添加比例尺
def add_scalebar(ax, lon0, lat0, length, linewidth=2, fontsize=18):
    ax.hlines(y=lat0, xmin=lon0, xmax=lon0 + length / 111, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.vlines(x=lon0 + length / 111, ymin=lat0 - 0.1, ymax=lat0 + 0.1, colors="black", ls="-", lw=linewidth)
    ax.text(lon0 + (length / 111) / 2, lat0 + 0.2, f"{length} km", horizontalalignment='center', fontsize=fontsize)

# 函数：添加指北针
def add_north_arrow(ax, lon, lat, length=1.0, width=0.2, head_width=0.4, head_length=0.4, fontsize=18):
    ax.add_patch(FancyArrow(
        lon, lat, 0, length,  # 起点 (lon, lat) 和箭头方向 (0, length)
        width=width, head_width=head_width, head_length=head_length, color='black'
    ))
    ax.text(lon, lat + length + 1, 'N', ha='center', va='center', fontsize=fontsize, color='black')

# 读取综合等级数据
grades_file_path = r'D:\A-Projects\DWAA Project\Station_Grades.csv'
grades_df = pd.read_csv(grades_file_path)

# 获取站点的经纬度和等级数据
station_ids = grades_df["Station_ID"].values
lats = grades_df["Latitude"].values
lons = grades_df["Longitude"].values
dry_to_wet_grades = grades_df["Dry_to_Wet_Grade"].values
wet_to_dry_grades = grades_df["Wet_to_Dry_Grade"].values

# 加载中国边界文件
china_boundary = cfeature.ShapelyFeature(
    Reader(r'D:\A-Projects\DWAA Project\Shapefile\Northern China SubRegion.shp').geometries(),
    ccrs.PlateCarree(),
    edgecolor='black',  # Set the color of the boundary lines
    linewidth=1,
    facecolor="#FFFFFF"  # Adjust the line width as needed
)

grade_colors = {1: '#99CCFF', 2: '#FFFF66', 3: '#FF8000', 4: '#660000'}  # 可根据需求调整颜色
point_size = 24

# 创建一个包含两个子图的绘图（上下排列）
fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(16, 6))
plot_labels = ['a', 'b', 'c', 'd']
# 绘制干转涝等级地图
ax1.add_feature(china_boundary)
ax1.set_extent([72, 136, 30, 53])

# 根据干转涝等级颜色绘制站点
for grade in np.unique(dry_to_wet_grades):
    mask = dry_to_wet_grades == grade
    ax1.scatter(lons[mask], lats[mask], color=grade_colors[grade], s=point_size, label=f'Level {grade}')
ax1.set_title("DTW", fontsize=22)
ax1.legend( loc='upper center',fontsize=18, frameon=False)
# 添加地图三要素
add_scalebar(ax1, lon0=73, lat0=31, length=500, linewidth=2, fontsize=16)
add_north_arrow(ax1, lon=130, lat=52, length=2.0, fontsize=16)
ax1.set_xticks(range(75, 140, 10), crs=ccrs.PlateCarree())
ax1.set_yticks(range(30, 55, 5), crs=ccrs.PlateCarree())
ax1.tick_params(axis='both', labelsize=18, direction='in', length=5)
ax1.text(0.02, 0.98, plot_labels[1], transform=ax1.transAxes,
            fontsize=24, fontweight='bold', va='top', ha='left')
# 绘制涝转干等级地图
ax2.add_feature(china_boundary)
ax2.set_extent([72, 136, 30, 53])

# 根据涝转干等级颜色绘制站点
for grade in np.unique(wet_to_dry_grades):
    mask = wet_to_dry_grades == grade
    ax2.scatter(lons[mask], lats[mask], color=grade_colors[grade], s=point_size, label=f'Level {grade}')
ax2.set_title("WTD", fontsize=22)
ax2.legend( loc='upper center' ,fontsize=18, frameon=False)
# 添加地图三要素
add_scalebar(ax2, lon0=73, lat0=31, length=500, linewidth=2, fontsize=16)
add_north_arrow(ax2, lon=130, lat=52, length=2.0, fontsize=16)
ax2.set_xticks(range(75, 140, 10), crs=ccrs.PlateCarree())
ax2.set_yticks(range(30, 55, 5), crs=ccrs.PlateCarree())
ax2.tick_params(axis='both', labelsize=18, direction='in', length=5)
ax2.text(0.02, 0.98, plot_labels[2], transform=ax2.transAxes,
            fontsize=24, fontweight='bold', va='top', ha='left')
# 调整布局
plt.tight_layout()
output_path = r'D:\A-Projects\DWAA Project\Figure\Grade_DWAA.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')

plt.show()





