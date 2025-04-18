import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 14})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# 读取数据
total_dwaa_df = pd.read_csv(r'D:\A-Projects\DWAA Project\total_dwaa_counts.csv')

# 提取纬度和事件数量
lats = total_dwaa_df["Latitude"].values
dry_to_wet_counts = total_dwaa_df["Dry_To_Wet_Count"].values
wet_to_dry_counts = total_dwaa_df["Wet_To_Dry_Count"].values

# 定义纬度区间（例如35度到53度，间隔5度）
latitude_bins = np.arange(30, 54, 1)
latitude_labels = [f"{int(bin_start)}-{int(bin_start+1)}" for bin_start in latitude_bins[:-1]]

# 按纬度区间统计旱转涝和涝转旱事件数量
dry_to_wet_by_latitude = []
wet_to_dry_by_latitude = []
stations_per_bin = []

for i in range(len(latitude_bins) - 1):
    bin_start = latitude_bins[i]
    bin_end = latitude_bins[i + 1]
    
    # 筛选当前纬度区间的数据
    bin_indices = (lats >= bin_start) & (lats < bin_end)
    
    # 统计该区间内的站点数量
    stations_in_bin = bin_indices.sum()
    
    # 计算该区间内旱转涝和涝转旱的总数量
    dry_to_wet_by_latitude.append(dry_to_wet_counts[bin_indices].sum())
    wet_to_dry_by_latitude.append(wet_to_dry_counts[bin_indices].sum())
    stations_per_bin.append(stations_in_bin)

# 计算每个区间的平均事件数量（总事件数 / 站点数）
avg_dry_to_wet_by_latitude = [dry_to_wet / stations for dry_to_wet, stations in zip(dry_to_wet_by_latitude, stations_per_bin)]
avg_wet_to_dry_by_latitude = [wet_to_dry / stations for wet_to_dry, stations in zip(wet_to_dry_by_latitude, stations_per_bin)]

# 绘制折线图
fig, ax = plt.subplots(figsize=(12, 8))

x = np.arange(len(latitude_labels))

# 绘制两条折线
ax.plot(x, avg_dry_to_wet_by_latitude, marker='o', label="Dry to Wet", color='#66B2FF', linestyle='-')
ax.plot(x, avg_wet_to_dry_by_latitude, marker='s', label="Wet to Dry", color='#FFB266', linestyle='--')

# 设置图例和标签
ax.set_xlabel("Latitude Range (°N)")
ax.set_ylabel("Average Count per Station")
ax.set_xticks(x)
ax.set_xticklabels(latitude_labels, rotation=45)
ax.legend()
# Save the figure to a file
output_path = r'D:\A-Projects\DWAA Project\Figure\DWAA_Latitude_Count.png'
plt.savefig(output_path, dpi=300)
# 显示图形
plt.tight_layout()
plt.show()
