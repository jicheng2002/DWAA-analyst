from PIL import Image
import os

# 获取桌面路径（适用于 Windows 和 Mac/Linux）
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 指定两张待拼接的图片路径（请修改为你的图片路径）
image_path_1 = "image1.jpg"  # 第一张图片路径
image_path_2 = "image2.jpg"  # 第二张图片路径

# 打开图片
img1 = Image.open(image_path_1)
img2 = Image.open(image_path_2)

# 确保两张图片的宽度一致
if img1.width != img2.width:
    raise ValueError("两张图片的宽度不一致，请调整后再拼接！")

# 计算新图像的尺寸
new_width = img1.width
new_height = img1.height + img2.height

# 创建新的空白图像（RGB模式）
new_img = Image.new("RGB", (new_width, new_height))

# 粘贴两张图片到新图像上
new_img.paste(img1, (0, 0))  # 第一张图片放在顶部
new_img.paste(img2, (0, img1.height))  # 第二张图片放在第一张图片下面

# 保存最终图片到桌面
output_path = os.path.join(desktop_path, "merged_image.jpg")
new_img.save(output_path)

print(f"拼接完成！图片已保存到: {output_path}")
