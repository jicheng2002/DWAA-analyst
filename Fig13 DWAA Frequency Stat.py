import os
import pandas as pd
import matplotlib.pyplot as plt

# 设置全局字体
plt.rcParams.update({'font.size': 22})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# 文件夹路径
folder_path = r"D:\A-Projects\DWAA Project\DWAA_Seasons_Stations"
output_path = r"D:\A-Projects\DWAA Project\Figure"

# 季节和事件类型
seasons = ["Spring", "Summer", "Fall", "Winter"]
event_types = ["DTW", "WTD"]
sheet = "Count"
plot_labels = ['c', 'd']
# 初始化字典存储数据
data = {event: {season: None for season in seasons} for event in event_types}

# 遍历事件类型和季节，读取数据
for event_type in event_types:
    for season in seasons:
        # 构造文件路径
        file_name = f"{event_type}_{season}.xlsx"
        file_path = os.path.join(folder_path, file_name)

        # 读取指定工作表的数据
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=sheet)

            # 检查是否包含所需的列
            if "FID_\u4e2d\u56fd" in df.columns and "MEAN" in df.columns:
                # 存储数据到字典
                data[event_type][season] = df[["FID_\u4e2d\u56fd", "MEAN"]]

# 创建子图
fig, axes = plt.subplots(1, 2, figsize=(18, 5))  # 调整大小

plot_idx = 0
for event_type in event_types:
    ax = axes[plot_idx]
    for fid in range(6):  # 假设有 6 个子区域 (FID_中国: 0-5)
        mean_values = []
        for season in seasons:
            df = data[event_type][season]
            if df is not None and fid in df["FID_\u4e2d\u56fd"].values:
                mean_value = df.loc[df["FID_\u4e2d\u56fd"] == fid, "MEAN"].values[0]
                mean_values.append(mean_value)
            else:
                mean_values.append(0)  # 如果没有数据，默认值为 0
        ax.plot(seasons, mean_values, marker="o",label=f"Subregion {fid + 1}", linewidth=3, markersize='12')  # 横轴为季节
    ax.set_title(f"{event_type.upper()}")
    ax.set_xlabel("Seasons")
    ax.set_ylabel("Frequency")
    ax.text(0.02, 0.98, plot_labels[plot_idx], transform=ax.transAxes,
            fontsize=24, fontweight='bold', va='top', ha='left')
    plot_idx += 1

# 调整子图布局
plt.subplots_adjust(left=0.05, right=0.98, top=0.90, bottom=0.08, hspace=0.3, wspace=0.15)


# 保存图像
plt.savefig(os.path.join(output_path, "Frequency_Visualization_Per_Subregion.png"), dpi=300)
plt.show()


import os
import pandas as pd
import matplotlib.pyplot as plt

# 设置全局字体
plt.rcParams.update({'font.size': 22})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# 定义文件夹路径
folder_path = r"D:\A-Projects\DWAA Project\DWAA_Decades_Stations"
output_path = r"D:\A-Projects\DWAA Project\Figure"

# 定义年代及对应的标签
decades = ["8090", "9000", "0010", "1020"]
decade_labels = ["1980-1990", "1990-2000", "2000-2010", "2010-2020"]
plot_labels = ['a', 'b']
event_types = ["DTW", "WTD"]  # 事件类型
sheet = "Count"  # 只读取 'Count' 表

# 初始化数据字典
data = {event: {decade: None for decade in decades} for event in event_types}

# 读取数据
target_columns = ["ZONE-CODE", "MEAN"]
for event_type in event_types:
    for decade in decades:
        file_name = f"{event_type}_{decade}.xlsx"
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=sheet)
            if all(col in df.columns for col in target_columns):
                data[event_type][decade] = df[target_columns]

# 绘制数据
fig, axes = plt.subplots(1, 2, figsize=(18, 5))  # 两个子图
for idx, event_type in enumerate(event_types):
    ax = axes[idx]
    for fid in range(6):  # 假设有6个子区域 (ZONE-CODE: 1-6)
        mean_values = []
        for decade in decades:
            df = data[event_type][decade]
            if df is not None:
                df["ZONE-CODE"] = df["ZONE-CODE"].astype(int)
                mean_value = df.loc[df["ZONE-CODE"] == fid + 1, "MEAN"].values[0] if (fid + 1) in df["ZONE-CODE"].values else 0
            else:
                mean_value = 0
            mean_values.append(mean_value)
        ax.plot(decade_labels, mean_values, marker="o", label=f"Subregion {fid + 1}", linewidth=3, markersize=12)
    ax.set_title(f"{event_type.upper()} ")
    ax.set_xlabel("Decades")
    ax.set_ylabel("Frequency")
    ax.text(0.02, 0.98, plot_labels[idx], transform=ax.transAxes,
            fontsize=24, fontweight='bold', va='top', ha='left')
    ax.grid(False)

# 调整布局
plt.subplots_adjust(left=0.05, right=0.98, top=0.90, bottom=0.08, hspace=0.3, wspace=0.15)

# 保存图像
plt.savefig(os.path.join(output_path, "Decadal_Frequency_Visualization_Per_Subregion.png"), dpi=300)
plt.show()
