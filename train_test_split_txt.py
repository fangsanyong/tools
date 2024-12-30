import os
import random
from pathlib import Path

# Define the directory where images are stored
image_dir = Path('E:/fsy/hedao/hedao_dataset')  # Replace with your actual path

# Collect all image files in the directory
image_files = [str(file) for file in image_dir.glob('**/*.jpg') if file.is_file()]  # Adjust the extension if necessary

# Shuffle the list to ensure random distribution
random.shuffle(image_files)

# Define the split ratio (e.g., 80% train, 20% validation)
train_ratio = 0.8
train_size = int(len(image_files) * train_ratio)

# Split the list
train_files = image_files[:train_size]
val_files = image_files[train_size:]

# Write to train.txt
with open('train.txt', 'w') as f:
    for file in train_files:
        f.write(f"{file}\n")

# Write to val.txt
with open('val.txt', 'w') as f:
    for file in val_files:
        f.write(f"{file}\n")

print(f"Total images: {len(image_files)}")
print(f"Train images: {len(train_files)}")
print(f"Validation images: {len(val_files)}")