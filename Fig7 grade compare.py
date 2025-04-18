import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# 读取CSV文件
grades_df = pd.read_csv(r"D:\A-Projects\DWAA Project\Station_Grades.csv")

# 计算旱转涝和涝转旱等级的数量
dry_to_wet_counts = grades_df['Dry_to_Wet_Grade'].value_counts().sort_index()
wet_to_dry_counts = grades_df['Wet_to_Dry_Grade'].value_counts().sort_index()

# 创建一个包含一张图的布局
fig, ax = plt.subplots(figsize=(18, 6))

# 设置柱形图的宽度
bar_width = 0.35

# 设置位置
index = dry_to_wet_counts.index

# 绘制旱转涝柱状图
ax.bar(index - bar_width/2, dry_to_wet_counts.values, bar_width, color='skyblue', edgecolor='black', label='DTW')

# 绘制涝转旱柱状图
ax.bar(index + bar_width/2, wet_to_dry_counts.values, bar_width, color='salmon', edgecolor='black', label='WTD')

ax.set_xlabel('Level')
ax.set_ylabel('Count')
plot_labels = ['a', 'b', 'c', 'd']
# 设置x轴为整数等级1, 2, 3, 4
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels([1, 2, 3, 4])
ax.text(0.02, 0.98, plot_labels[0], transform=ax.transAxes,
            fontsize=24, fontweight='bold', va='top', ha='left')
# 添加图例
ax.legend()

# 自动调整布局以防止重叠
plt.tight_layout()
plt.show()
