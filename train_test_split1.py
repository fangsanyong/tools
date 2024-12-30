import os
import shutil
import random

# 配置路径
# 配置路径
images_folder = "E:/fsy/hedao/hedao_dataset"
labels_folder = "E:/fsy/hedao/hedao_dataset"

output_train_folder = "E:/fsy/hedao/train"  # 训练集文件夹
output_val_folder = "E:/fsy/hedao/val"  # 验证集文件夹
train_ratio = 0.8  # 训练集比例（比如 80%）

# 创建输出文件夹
os.makedirs(os.path.join(output_train_folder, "images"), exist_ok=True)
os.makedirs(os.path.join(output_train_folder, "labels"), exist_ok=True)
os.makedirs(os.path.join(output_val_folder, "images"), exist_ok=True)
os.makedirs(os.path.join(output_val_folder, "labels"), exist_ok=True)

# 获取所有图片文件（支持多种图片格式）
image_files = [f for f in os.listdir(images_folder) if f.endswith((".jpg", ".JPG", ".png", ".jpeg"))]

# 打乱数据顺序
random.shuffle(image_files)

# 按比例划分训练集和验证集
train_count = int(len(image_files) * train_ratio)
train_files = image_files[:train_count]
val_files = image_files[train_count:]

# 将文件复制到对应的文件夹
def move_files(file_list, target_image_folder, target_label_folder):
    for image_file in file_list:
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + ".txt"

        # 移动图片文件
        image_src = os.path.join(images_folder, image_file)
        image_dst = os.path.join(target_image_folder, image_file)
        if os.path.exists(image_src):
            shutil.copy(image_src, image_dst)

        # 移动标签文件
        label_src = os.path.join(labels_folder, label_file)
        label_dst = os.path.join(target_label_folder, label_file)
        if os.path.exists(label_src):
            shutil.copy(label_src, label_dst)

# 移动训练集文件
move_files(train_files, os.path.join(output_train_folder, "images"), os.path.join(output_train_folder, "labels"))

# 移动验证集文件
move_files(val_files, os.path.join(output_val_folder, "images"), os.path.join(output_val_folder, "labels"))

print(f"数据集划分完成！训练集：{len(train_files)}，验证集：{len(val_files)}")
