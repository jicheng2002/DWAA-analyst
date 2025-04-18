# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 18})
# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman']
# # Define the folder containing Excel files
# folder_path = r"D:\A-Projects\DWAA Project\DWAA_Decades_Stations"
# output_path = r"D:\A-Projects\DWAA Project\Figure"

# # Define decades and corresponding folder names
# decades = ["8090", "9000", "0010", "1020"]  # Corresponds to 1980-1990, 1990-2000, etc.
# event_types = ["DTW", "WTD"]  # Use abbreviated event types
# sheets = ["Count", "IA", "IU"]

# # Initialize a dictionary to store the data
# data = {sheet: {event: {decade: None for decade in decades} for event in event_types} for sheet in sheets}

# # Loop over event types and sheets to read data
# for sheet in sheets:
#     for event_type in event_types:
#         for decade in decades:
#             # Determine file path
#             file_name = f"{event_type}_{decade}.xlsx"
#             file_path = os.path.join(folder_path, file_name)

#             # Read the relevant sheet
#             if os.path.exists(file_path):
#                 df = pd.read_excel(file_path, sheet_name=sheet)

#                 # Check if the required columns exist
#                 if "ZONE-CODE" in df.columns and "MEAN" in df.columns:
#                     if event_type == "DTW" and sheet in ["IA", "IU"]:
#                         df["MEAN"] = df["MEAN"] * 2
#                     # Store the data in the dictionary
#                     data[sheet][event_type][decade] = df[["ZONE-CODE", "MEAN"]]

# # Plotting the data
# fig, axes = plt.subplots(2, 3, figsize=(18, 12), constrained_layout=True)

# plot_idx = 0
# for sheet in sheets:
#     for event_type in event_types:
#         ax = axes[plot_idx // 3, plot_idx % 3]
#         for fid in range(6):  # Assuming 6 subregions (ZONE-CODE: 1-6)
#             mean_values = []
#             for decade in decades:
#                 df = data[sheet][event_type][decade]
#                 if df is not None:
#                     # Ensure `ZONE-CODE` is an integer for comparison
#                     df["ZONE-CODE"] = df["ZONE-CODE"].astype(int)
#                     if fid + 1 in df["ZONE-CODE"].values:  # Adjust fid for 1-based indexing
#                         mean_value = df.loc[df["ZONE-CODE"] == fid + 1, "MEAN"].values[0]
#                         mean_values.append(mean_value)
#                     else:
#                         mean_values.append(0)
#                 else:
#                     mean_values.append(0)  # Default to 0 if no data
#             ax.plot(mean_values, decades, marker="o", label=f"Subregion {fid}")
#         ax.set_title(f"{event_type} - {sheet}")  # Use abbreviated event type in the title
#         ax.set_xlabel("MEAN Value")
#         ax.set_ylabel("Decades")
#         plot_idx += 1

# plt.tight_layout()
# plt.savefig(os.path.join(output_path, "Decadal_MEAN_Visualization_Per_Subregion.png"))
# plt.show()

# # Extract legend handles and labels
# handles, labels = ax.get_legend_handles_labels()

# # Create a separate figure for the legend (vertically aligned)
# legend_fig = plt.figure(figsize=(3, 10))
# legend_ax = legend_fig.add_subplot(111)
# legend_ax.axis("off")  # Turn off the axis
# legend_ax.legend(handles, labels, loc="center", ncol=1, fontsize=10)  # ncol=1 for vertical alignment


# # Save and show the legend as a separate image
# legend_fig.savefig(os.path.join(output_path, "Legend.png"))



# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# # 设置全局字体
# plt.rcParams.update({'font.size': 24})
# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman']

# # Define the folder containing Excel files
# folder_path = r"D:\A-Projects\DWAA Project\DWAA_Decades_Stations"
# output_path = r"D:\A-Projects\DWAA Project\Figure"

# # Define decades and corresponding folder names
# decades = ["8090", "9000", "0010", "1020"]  # Corresponds to 1980-1990, 1990-2000, etc.
# event_types = ["DTW", "WTD"]  # Use abbreviated event types
# sheets = ["Count", "IA", "IU"]

# # Initialize a dictionary to store the data
# data = {sheet: {event: {decade: None for decade in decades} for event in event_types} for sheet in sheets}

# # Loop over event types and sheets to read data
# for sheet in sheets:
#     for event_type in event_types:
#         for decade in decades:
#             # Determine file path
#             file_name = f"{event_type}_{decade}.xlsx"
#             file_path = os.path.join(folder_path, file_name)

#             # Read the relevant sheet
#             if os.path.exists(file_path):
#                 df = pd.read_excel(file_path, sheet_name=sheet)

#                 # Check if the required columns exist
#                 if "ZONE-CODE" in df.columns and "MEAN" in df.columns:
#                     if event_type == "DTW" and sheet in ["IA", "IU"]:
#                         df["MEAN"] = df["MEAN"] * 2
#                     # Store the data in the dictionary
#                     data[sheet][event_type][decade] = df[["ZONE-CODE", "MEAN"]]

# # Plotting the data
# fig, axes = plt.subplots(2, 3, figsize=(20, 12))  # 增加了整体高度以容纳图例

# plot_idx = 0
# for sheet in sheets:
#     for event_type in event_types:
#         ax = axes[plot_idx // 3, plot_idx % 3]
#         for fid in range(6):  # Assuming 6 subregions (ZONE-CODE: 1-6)
#             mean_values = []
#             for decade in decades:
#                 df = data[sheet][event_type][decade]
#                 if df is not None:
#                     # Ensure `ZONE-CODE` is an integer for comparison
#                     df["ZONE-CODE"] = df["ZONE-CODE"].astype(int)
#                     if fid + 1 in df["ZONE-CODE"].values:  # Adjust fid for 1-based indexing
#                         mean_value = df.loc[df["ZONE-CODE"] == fid + 1, "MEAN"].values[0]
#                         mean_values.append(mean_value)
#                     else:
#                         mean_values.append(0)
#                 else:
#                     mean_values.append(0)  # Default to 0 if no data
#             ax.plot(decades, mean_values, marker="o", label=f"Subregion {fid + 1}")  # Decades as x-axis
#             # 修改标题代码，动态替换 "Count" 为 "Frequency"
#         ax.set_title(f"{event_type.capitalize()} - {'Frequency' if sheet == 'Count' else sheet}")
#         ax.set_xlabel("Decades")
#         ax.set_ylabel("MEAN Value")
#         ax.grid(False)
#         plot_idx += 1

# # 调整子图之间的布局
# plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15, hspace=0.3, wspace=0.3)

# # 提取图例句柄和标签
# handles, labels = ax.get_legend_handles_labels()

# # 在主图最下面添加图例
# fig.legend(handles, labels, loc='lower center', ncol=6, fontsize=24, frameon=False)  # 横向排列 (ncol=6)

# # 保存图像
# plt.savefig(os.path.join(output_path, "Decadal_MEAN_Visualization_Per_Subregion.png"), dpi=300)
# plt.show()



import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体
plt.rcParams.update({'font.size': 24})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# Define the folder containing Excel files
folder_path = r"D:\A-Projects\DWAA Project\DWAA_Decades_Stations"
output_path = r"D:\A-Projects\DWAA Project\Figure"

# Define decades and corresponding folder names
decades = ["8090", "9000", "0010", "1020"]  # Corresponds to 1980-1990, 1990-2000, etc.
decade_labels = ["1980-1990", "1990-2000", "2000-2010", "2010-2020"]  # Full range labels
event_types = ["DTW", "WTD"]  # Use abbreviated event types
sheets = ["IA", "IU"]
# Initialize a dictionary to store the data
data = {sheet: {event: {decade: None for decade in decades} for event in event_types} for sheet in sheets}

# Loop over event types and sheets to read data
for sheet in sheets:
    for event_type in event_types:
        for decade in decades:
            # Determine file path
            file_name = f"{event_type}_{decade}.xlsx"
            file_path = os.path.join(folder_path, file_name)

            # Read the relevant sheet
            if os.path.exists(file_path):
                df = pd.read_excel(file_path, sheet_name=sheet)

                # Check if the required columns exist
                if "ZONE-CODE" in df.columns and "MEAN" in df.columns:
                    if event_type == "DTW" and sheet in ["IA", "IU"]:
                        df["MEAN"] = df["MEAN"] * 2
                    if event_type == "WTD" and sheet in ["IA", "IU"]:
                        df["MEAN"] = abs(df["MEAN"])  # Take absolute values
                    # Store the data in the dictionary
                    data[sheet][event_type][decade] = df[["ZONE-CODE", "MEAN"]]

# Determine unified IA and IU value ranges
ia_min = min(
    min(data["IA"]["DTW"][decade]["MEAN"].min() for decade in decades if data["IA"]["DTW"][decade] is not None),
    min(data["IA"]["WTD"][decade]["MEAN"].min() for decade in decades if data["IA"]["WTD"][decade] is not None)
)
ia_max = max(
    max(data["IA"]["DTW"][decade]["MEAN"].max() for decade in decades if data["IA"]["DTW"][decade] is not None),
    max(data["IA"]["WTD"][decade]["MEAN"].max() for decade in decades if data["IA"]["WTD"][decade] is not None)
)
iu_min = min(
    min(data["IU"]["DTW"][decade]["MEAN"].min() for decade in decades if data["IU"]["DTW"][decade] is not None),
    min(data["IU"]["WTD"][decade]["MEAN"].min() for decade in decades if data["IU"]["WTD"][decade] is not None)
)
iu_max = max(
    max(data["IU"]["DTW"][decade]["MEAN"].max() for decade in decades if data["IU"]["DTW"][decade] is not None),
    max(data["IU"]["WTD"][decade]["MEAN"].max() for decade in decades if data["IU"]["WTD"][decade] is not None)
)

# Create 2x2 subplots for IA and IU (DTW and WTD)
fig, axes = plt.subplots(2, 2, figsize=(18, 10))  # Adjust size for a 2x2 layout
plot_labels = ['a', 'b', 'c', 'd']  # Subplot labels

plot_idx = 0
for sheet in sheets:
    for event_type in event_types:
        ax = axes[plot_idx // 2, plot_idx % 2]
        for fid in range(6):  # Assuming 6 subregions (ZONE-CODE: 1-6)
            mean_values = []
            for decade in decades:
                df = data[sheet][event_type][decade]
                if df is not None:
                    # Ensure `ZONE-CODE` is an integer for comparison
                    df["ZONE-CODE"] = df["ZONE-CODE"].astype(int)
                    if fid + 1 in df["ZONE-CODE"].values:  # Adjust fid for 1-based indexing
                        mean_value = df.loc[df["ZONE-CODE"] == fid + 1, "MEAN"].values[0]
                        mean_values.append(mean_value)
                    else:
                        mean_values.append(0)
                else:
                    mean_values.append(0)  # Default to 0 if no data
            ax.plot(decade_labels, mean_values, marker="o", label=f"Subregion {fid + 1}", linewidth=3, markersize='8')  # Decade labels as x-axis

        # Apply consistent value ranges
        if sheet == "IA":
            ax.set_ylim(ia_min-0.2, ia_max+0.4)  # Consistent IA range
        elif sheet == "IU":
            ax.set_ylim(iu_min-0.2, iu_max+0.4)  # Consistent IU range

        ax.set_title(f"{event_type.upper()} - {sheet}")
        ax.set_ylabel("Intensity")
        ax.grid(False)
        # Add label in the top-left corner of each subplot
        ax.text(0.02, 0.98, plot_labels[plot_idx], transform=ax.transAxes,
                fontsize=24, fontweight='bold', va='top', ha='left')
        plot_idx += 1

# Adjust layout
plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.08, hspace=0.3, wspace=0.15)

# Extract legend handles and labels
handles, labels = ax.get_legend_handles_labels()


# Save the plot
plt.savefig(os.path.join(output_path, "Decadal_MEAN_Visualization_2x2.png"), dpi=300)
plt.show()
