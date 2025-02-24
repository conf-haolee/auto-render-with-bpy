import os
import cv2
import numpy as np

class RenderPicStandardization:
    def __init__(self, render_pic_path):
        self._render_pic_path = render_pic_path

    @property
    def render_pic_path(self):
        return self._render_pic_path
    @render_pic_path.setter
    def render_pic_path(self, render_pic_path):
        self._render_pic_path = render_pic_path

    def get_latest_directory(self):
        # 获取当前目录
        current_directory = self._render_pic_path
        # 获取当前目录下的所有文件夹
        directories = [d for d in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, d))]
        # 按修改时间排序，获取最新的文件夹
        latest_directory = max(directories, key=lambda d: os.path.getmtime(os.path.join(current_directory, d)))
        print(f"最新的文件夹是: {latest_directory}")
        latest_directory_path = os.path.join(current_directory, latest_directory)
        return latest_directory_path
    
     # 删除非单连通域的图片
    def del_not_single_connection(self):
        latest_render_pic_path = self.get_latest_directory()
        # 获取当前目录下的所有文件夹
        directories = [d for d in os.listdir(latest_render_pic_path) if os.path.isdir(os.path.join(latest_render_pic_path, d))]
        # 获取文件夹的数量
        folder_count = len(directories)
        for index  in range(1,folder_count + 1):
            label_folder_path = latest_render_pic_path + '/num_' + str(index)  # 替换为你的文件夹路径
            for filename in os.listdir(label_folder_path):
                    file_path = os.path.join(label_folder_path, filename)
                    # 检查是否为图片格式
                    if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
                        # 读取图像
                        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                        # 全局阈值分割
                        _, binary_image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)
                        # 查找连通域
                        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
                        if num_labels == 2:  # 是单一连通域
                            pass
                            # print(f"Retained grayscale image: {file_path}")
                        else:
                            # 如果不是单一连通域，则删除
                            os.remove(file_path)
                            print(f"Deleted color image: {file_path}")

    def torus_position_normalization(self):
        pass

    def standardize(self):
        # Standardize the render pic
        self.del_not_single_connection()
        self.torus_position_normalization()

        # return self.render_pic

# def generate_circle_positions(radius, x1, y1, xlim = (-1,1), ylim = (5,7)):
#     """
#     随机生成两个相交或相切的圆的圆心坐标
#     :param radius: 圆的半径
#     :param xlim: x 轴的取值范围
#     :param ylim: y 轴的取值范围
#     :return: (x2, y2) 两个圆心坐标
#     """
#     while True:
#         # 生成圆心距离 d，确保 0 < d ≤ 2r
#         d = np.random.uniform(0.1, 2 * radius)  

#         # 生成随机角度 θ
#         theta = np.random.uniform(0, 2 * np.pi)

#         # 计算第二个圆心坐标
#         x2 = x1 + d * np.cos(theta)
#         y2 = y1 + d * np.sin(theta)

#         # 确保第二个圆心仍然在范围内
#         if (xlim[0] + radius <= x2 <= xlim[1] - radius) and (ylim[0] + radius <= y2 <= ylim[1] - radius):
#             return (x1, y1), (x2, y2)
        