import os
import cv2
import random

# 配置路径
images_folder = "E:/fsy/hedao/"
labels_folder = "E:/fsy/hedao/"
result_folder = "E:/fsy/result"
classes_file = "E:/fsy/classes.txt"  # 类别名称文件

images_folder = "E:/sdsdsd/pic1/"
labels_folder = "E:/sdsdsd/pic1/"
result_folder = "E:/fsy/tools/result"
classes_file = "E:/sdsdsd//cls.txt"  # 类别名称文件

# 检查结果文件夹是否存在，不存在则创建
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# 读取类别名称
with open(classes_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# # 为每个类别生成随机颜色
# #class_colors = {class_id: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for class_id in range(len(classes))}
 
class_colors = {
    0: (255, 0, 0),  # Red
    1: (0, 255, 0),  # Green
    2: (0, 0, 255),  # Blue
    3: (255, 150, 0),  # Orange
    4: (255, 200, 0),  # Light Orange
    5: (255, 255, 0),  # Yellow
    6: (200, 255, 0),  # Light Green-Yellow
    7: (150, 255, 0),  # Yellow-Green
    8: (100, 255, 0),  # Chartreuse
    9: (50, 255, 0),  # Lime
    10: (0, 255, 50),  # Light Green
    11: (0, 255, 100), # Bright Green
    12: (0, 255, 150), # Green-Yellow
    13: (0, 255, 200), # Aqua Green
    14: (0, 255, 255), # Cyan
    15: (0, 200, 255), # Sky Blue
    16: (0, 150, 255), # Light Blue
    17: (0, 100, 255), # Azure
    18: (0, 50, 255),  # Blue
    19: (50, 0, 255),  # Indigo
    20: (100, 0, 255), # Violet
    21: (150, 0, 255), # Purple
    22: (200, 0, 255), # Magenta
    23: (255, 0, 255), # Pink
    24: (255, 0, 200), # Hot Pink
    25: (255, 0, 150), # Dark Pink
    26: (255, 0, 100), # Coral
    27: (255, 0, 50),  # Red-Orange
    28: (255, 50, 50), # Light Red
    29: (255, 100, 100),# Salmon
    30: (255, 150, 150),# Light Salmon
    31: (255, 200, 200),# Pale Pink
    32: (200, 255, 50), # Light Yellow-Green
    33: (200, 255, 100),# Pale Chartreuse
    34: (200, 255, 150),# Light Yellow
    35: (200, 255, 200),# Pale Green
    36: (150, 255, 255),# Pale Cyan
    37: (100, 255, 255),# Light Cyan
    38: (50, 255, 255), # Pale Turquoise
    39: (50, 200, 255), # Light Sky Blue
    40: (100, 150, 255),# Light Blue
    41: (150, 100, 255),# Lavender
    42: (200, 50, 255), # Light Purple
    43: (255, 50, 255), # Light Magenta
    44: (255, 100, 255),# Light Pink
    45: (255, 150, 255),# Pale Pink
    46: (255, 200, 255),# Pale Violet Red
    47: (200, 255, 255),# Pale Turquoise
    48: (150, 255, 200),# Pale Green
    49: (100, 255, 150),# Light Green
    50: (50, 255, 100), # Light Lime
    51: (0, 255, 50),   # Bright Green
    52: (0, 200, 0),    # Dark Green
    53: (0, 150, 0),    # Forest Green
    54: (0, 100, 0),    # Dark Olive Green
    55: (0, 50, 0),     # Dark Moss Green
    56: (50, 0, 0),     # Maroon
    57: (100, 0, 0),    # Dark Red
    58: (150, 0, 0),    # Crimson
    59: (200, 0, 0),    # Scarlet
    60: (255, 0, 50),   # Bright Red
    61: (255, 50, 100), # Tomato
    62: (255, 100, 150),# Light Coral
    63: (255, 150, 200),# Pink
    64: (200, 255, 255),# Light Cyan
    65: (150, 200, 255),# Light Sky Blue
    66: (100, 150, 255),# Light Blue
    67: (50, 100, 255), # Cornflower Blue
    68: (0, 50, 255),   # Royal Blue
    69: (50, 0, 255),   # Deep Purple
    70: (100, 0, 200),  # Dark Violet
    71: (150, 0, 150),  # Purple
    72: (200, 0, 100),  # Medium Violet Red
    73: (255, 0, 50),   # Red
    74: (255, 50, 0),   # Orange Red
    75: (255, 100, 0),  # Dark Orange
    76: (255, 150, 0),  # Orange
    77: (255, 200, 0),  # Gold
    78: (200, 255, 0),  # Yellow Green
    79: (150, 255, 0)   # Lime Green
}
    
def draw_bounding_boxes(image_path, label_path, output_path):
    # 读取图片
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # 读取标签文件
    with open(label_path, "r") as f:
        lines = f.readlines()

    # 遍历标签文件的每一行
    for line in lines:
        values = line.strip().split()
        class_id = int(values[0])
        x_center, y_center, box_width, box_height = map(float, values[1:])

        # 计算边界框的左上角和右下角坐标
        x1 = int((x_center - box_width / 2) * width)
        y1 = int((y_center - box_height / 2) * height)
        x2 = int((x_center + box_width / 2) * width)
        y2 = int((y_center + box_height / 2) * height)

        # 画框
        color = class_colors[class_id]  # 根据类别获取颜色
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        # 显示类别名称
        label = classes[class_id]
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # 保存结果
    cv2.imwrite(output_path, image)

# 获取图片和标签文件列表
image_files = [f for f in os.listdir(images_folder) if f.endswith((".jpg", ".JPG", ".png", ".jpeg"))]
label_files = [f for f in os.listdir(labels_folder) if f.endswith(".txt")]


# 检查是否存在对应的图片文件
def find_image_for_label(base_name, image_folder):
    """
    查找标签文件对应的图片文件，支持多种后缀格式。
    """
    for ext in [".jpg", ".JPG", ".png", ".jpeg"]:
        image_path = os.path.join(image_folder, base_name + ext)
        if os.path.exists(image_path):
            return image_path
    return None  # 如果未找到对应的图片文件，返回 None

# 删除没有对应图片的标签文件
for label_file in label_files[:]:
    base_name = os.path.splitext(label_file)[0]
    image_path = find_image_for_label(base_name, images_folder)
    if not image_path:  # 如果没有找到对应的图片文件
        os.remove(os.path.join(labels_folder, label_file))
        label_files.remove(label_file)  # 从列表中移除
        print(f"删除没有对应图片的标签文件：{label_file}")

# 删除没有对应标签的图片文件
for image_file in image_files[:]:
    base_name = os.path.splitext(image_file)[0]
    label_file = base_name + ".txt"
    if not os.path.exists(os.path.join(labels_folder, label_file)):
        os.remove(os.path.join(images_folder, image_file))
        image_files.remove(image_file)  # 从列表中移除
        print(f"删除没有对应标签的图片文件：{image_file}")



# 遍历 images 文件夹下的所有图片
for image_file in image_files:
    image_path = os.path.join(images_folder, image_file)

    # 找到对应的标签文件
    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(labels_folder, label_file)

    # 检查标签文件是否存在
    if os.path.exists(label_path):
        output_path = os.path.join(result_folder, image_file)
        draw_bounding_boxes(image_path, label_path, output_path)
    else:
        print(f"标签文件缺失：{label_path}")