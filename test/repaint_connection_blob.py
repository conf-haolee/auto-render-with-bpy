import os
import cv2
import numpy as np
import glob

'''
    function: repaint_connection_blob
    description: 重新绘制连通域
    author: haolee
    time: 2025-02-08
    
'''

# Step 1: 生成一个白色背景图像
width, height = 512, 512
white_image = np.ones((height, width), dtype=np.uint8) * 255

# Step 2: 读取图片
image_folder = "D:/workspace/todo"
save_folder = "D:/workspace/done"
os.makedirs(save_folder, exist_ok=True)

image_files = glob.glob(os.path.join(image_folder, "*.*"))
image_files = [f for f in image_files if f.lower().endswith(("tif", "tiff", "gif", "bmp", "jpg", "jpeg", "jp2", "png", "pcx", "pgm", "ppm", "pbm", "xwd", "ima", "hobj"))]

for index, image_path in enumerate(image_files):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 阈值处理
    _, region = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY_INV)
    
    # 连接组件分析
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(region, connectivity=8)
    
    for j in range(1, num_labels):  # 跳过背景
        x, y, w, h, area = stats[j]
        
        # 选取当前连通域
        object_selected = labels == j
        
        # 裁剪出当前连通域
        image_reduced = np.zeros_like(gray_image)
        image_reduced[object_selected] = gray_image[object_selected]
        
        # 获取像素点
        y_coords, x_coords = np.where(object_selected)
        gray_values = gray_image[y_coords, x_coords]
        
        # 平移 blob
        x_coords = x_coords - x + 20
        y_coords = y_coords - y + 20
        
        # 生成新的白色背景
        new_white_image = np.ones((height, width), dtype=np.uint8) * 255
        
        # 设置新位置的像素值
        valid_indices = (x_coords >= 0) & (x_coords < width) & (y_coords >= 0) & (y_coords < height)
        new_white_image[y_coords[valid_indices], x_coords[valid_indices]] = gray_values[valid_indices]
        
        # 保存图片
        filename = os.path.join(save_folder, f"{index}_{j}.bmp")
        cv2.imwrite(filename, new_white_image)
