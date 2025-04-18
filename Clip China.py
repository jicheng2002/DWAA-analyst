import geopandas as gpd
from shapely.geometry import Polygon, LineString

# 输入线状 Shapefile 文件路径
input_shapefile = r"D:\A-Projects\DWAA Project\Shapefile\china_country.shp"  # 替换为实际路径
output_shapefile = r"D:\A-Projects\DWAA Project\Shapefile\CN_North_Boundary.shp"  # 输出文件路径

lines = gpd.read_file(input_shapefile, crs="EPSG:4326")  # 明确指定 CRS 为 WGS 84

# 过滤出北纬35度以北的线
lines = lines[lines.geometry.apply(lambda geom: geom.bounds[1] >= 35 or geom.bounds[3] >= 35)]

# 合并线条生成多边形（如果需要按属性区分，可以调整 groupby 的逻辑）
merged_lines = lines.unary_union

# 将北纬35度的线条扩展为多边形，假设生成凸包或缓冲区
polygon = Polygon(merged_lines)

# 创建 GeoDataFrame
gdf_polygon = gpd.GeoDataFrame({'geometry': [polygon]}, crs=lines.crs)

# 保存为 Shapefile
gdf_polygon.to_file(output_shapefile)

print("北纬35度以北的面状 Shapefile 已保存至:", output_shapefile)
