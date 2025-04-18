
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import rcParams
plt.rcParams.update({'font.size': 18})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# Define subregions and their corresponding colors
subregions = {
    1: 'Humid and Semi-humid Warm Temperate Zone of North China',
    2: 'Northwest Desert Area',
    3: 'Humid Subtropical Area of Central and South China',
    4: 'Humid and Semi-humid Temperate Zone of Northeast China',
    5: 'Inner Mongolia Grassland Area',
    6: 'Qinghai-Tibet Plateau',
}

color_list = ["#ff1f5b", "#f28522", "#009ade", "#af58ba",  "#ffc61e", "#00cd6c"]  # 颜色

# Create custom legend elements
legend_elements = [Line2D([0], [0], color=color, marker='o', linewidth=3, markersize='12', label=f"{id}: {name}")
                   for id, (name, color) in enumerate(zip(subregions.values(), color_list), 1)]

# Create the figure for the legend
fig, ax = plt.subplots(figsize=(12, 1))  # Adjust figure size for horizontal layout
ax.axis('off')  # Turn off the axes

# Add the horizontal legend
legend = ax.legend(
    handles=legend_elements, loc='center', fontsize=15, ncol=2,  # Horizontal layout with 4 columns
    frameon=False
)

# Adjust layout and save the figure
plt.tight_layout()
output_path = r"D:\A-Projects\DWAA Project\Figure\Horizontal_Subregion_Legend.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()



