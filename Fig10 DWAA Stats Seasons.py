
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体
plt.rcParams.update({'font.size': 24})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# 文件夹路径
folder_path = r"D:\A-Projects\DWAA Project\DWAA_Seasons_Stations"
output_path = r"D:\A-Projects\DWAA Project\Figure"

# 定义季节和事件类型
seasons = ["Spring", "Summer", "Fall", "Winter"]
event_types = ["DTW", "WTD"]
sheets = ["IA", "IU"]
marker_sizes = [10, 10, 10, 10, 10, 10]  # 每条线的点大小
# 初始化字典存储数据
data = {sheet: {event: {season: None for season in seasons} for event in event_types} for sheet in sheets}

# 遍历事件类型和季节，读取数据
for sheet in sheets:
    for event_type in event_types:
        for season in seasons:
            # 构造文件路径
            file_name = f"{event_type}_{season}.xlsx"
            file_path = os.path.join(folder_path, file_name)

            # 读取指定工作表的数据
            if os.path.exists(file_path):
                df = pd.read_excel(file_path, sheet_name=sheet)

                # 检查是否包含所需的列
                if "FID_中国" in df.columns and "MEAN" in df.columns:
                    if event_type == "DTW" and sheet in ["IA", "IU"]:
                        df["MEAN"] = df["MEAN"] * 2
                    if event_type == "WTD" and sheet in ["IA", "IU"]:
                        df["MEAN"] = abs(df["MEAN"])  # 取绝对值
                    # 存储数据到字典
                    data[sheet][event_type][season] = df[["FID_中国", "MEAN"]]

# 设置相同的IA和IU数值区间
ia_min = min(
    min(data["IA"]["DTW"][season]["MEAN"].min() for season in seasons),
    min(data["IA"]["WTD"][season]["MEAN"].min() for season in seasons)
)
ia_max = max(
    max(data["IA"]["DTW"][season]["MEAN"].max() for season in seasons),
    max(data["IA"]["WTD"][season]["MEAN"].max() for season in seasons)
)
iu_min = min(
    min(data["IU"]["DTW"][season]["MEAN"].min() for season in seasons),
    min(data["IU"]["WTD"][season]["MEAN"].min() for season in seasons)
)
iu_max = max(
    max(data["IU"]["DTW"][season]["MEAN"].max() for season in seasons),
    max(data["IU"]["WTD"][season]["MEAN"].max() for season in seasons)
)

# 创建 2x2 子图
fig, axes = plt.subplots(2, 2, figsize=(18, 10))  # 调整大小以适应 2x2 布局
plot_labels = ['e', 'f', 'g', 'h']  # Subplot labels

plot_idx = 0
for sheet in sheets:
    for event_type in event_types:
        ax = axes[plot_idx // 2, plot_idx % 2]
        for fid in range(6):  # 假设有 6 个子区域 (FID_中国: 0-5)
            mean_values = []
            for season in seasons:
                df = data[sheet][event_type][season]
                if df is not None and fid in df["FID_中国"].values:
                    mean_value = df.loc[df["FID_中国"] == fid, "MEAN"].values[0]
                    mean_values.append(mean_value)
                else:
                    mean_values.append(0)  # 如果没有数据，默认值为 0
            ax.plot(seasons, mean_values, marker="o",   label=f"Subregion {fid + 1}", linewidth=3, markersize='8')  # 横轴为季节

        # Apply consistent value ranges
        if sheet == "IA":
            ax.set_ylim(ia_min-0.2, ia_max+0.2)  # Consistent IA range
        elif sheet == "IU":
            ax.set_ylim(iu_min-0.2, iu_max+0.2)  # Consistent IU range

        ax.set_title(f"{event_type.upper()} - {sheet}")
        ax.set_ylabel("Intensity")
        # Add label in the top-left corner of each subplot
        ax.text(0.02, 0.98, plot_labels[plot_idx], transform=ax.transAxes,
                fontsize=24, fontweight='bold', va='top', ha='left')
        plot_idx += 1

# 调整子图布局
plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.08, hspace=0.3, wspace=0.15)

# 提取图例句柄和标签
handles, labels = ax.get_legend_handles_labels()

# 保存图像
plt.savefig(os.path.join(output_path, "Seasonal_MEAN_Visualization_2x2.png"), dpi=300)
plt.show()


