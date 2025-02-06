"""
    description: 测试qtdesginer ui 与 后端分离
    time:
    name: haolee 
"""
import sys
import os
import time
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow,QFileDialog, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice, Qt
from blender_scene import BlenderScene
from detect_real_ring import RealRingDetector

class ParaSettings(QMainWindow):
    def __init__(self):
        super(ParaSettings, self).__init__()
        # use uifile absolute path 
        current_dir = os.getcwd()
        ui_file_name = 'ui/para_settings.ui'
        absolute_path = os.path.join(current_dir, ui_file_name)
        
        ui_file = QFile(absolute_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {absolute_path}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        if not self.ui:
            print(loader.errorString())
            sys.exit(-1)
        # 设置ui界面标题和图标
        self.ui.setWindowTitle("密封圈视觉计数")
        icon_path = os.path.join(current_dir, 'ui/pic/ringVisionCount_logo3.png')
        self.ui.setWindowIcon(QIcon(icon_path))
        # # 创建并显示 SplashScreen
        # splash_path = os.path.join(current_dir, 'ui/pic/ringVisionCount_logo1.jpg')
        # splash = QSplashScreen(QPixmap(splash_path), Qt.WindowStaysOnTopHint)
        # splash.show()
        # # 模拟程序加载过程
        # time.sleep(2)  # 模拟加载时间 # 进度条QProgressBar 

        # 创建场景对象
        self._ring_scene = BlenderScene(2, 1, 0)  
        # 创建真实密封圈检测对象
        self._real_ring = RealRingDetector()

        # Connect the button click signal to the slot
        self.ui.start_render_btn.clicked.connect(self.handleCalc)

        self.ui.choose_save_image_path_btn.clicked.connect(self.handleChooseSaveImagePath)
        self.ui.load_image_path_btn.clicked.connect(self.handleLoadImagePath)

    # slot function: start render
    def handleCalc(self):
        print("Start Render!")
        print(self._ring_scene.save_image_folder_path)
        self._ring_scene.blender_render()
    # slot function: load real image path
    def handleLoadImagePath(self):
        print("Load Image Path!")
        load_image_path = QFileDialog.getExistingDirectory(self, "选择文件夹", os.path.expanduser("~"))
        if load_image_path:
            print("Selected Folder Path: ", load_image_path)
            self.ui.load_image_path_line.setText(load_image_path)
            self._real_ring.real_ring_image_path = load_image_path
            outer_radius, inner_radius = self._real_ring.detect()
            print("Average Max Radius:", outer_radius)
            print("Average Min Radius:", inner_radius)
            self.ui.outer_circle_radius_dspinbox.setValue(outer_radius)
            self.ui.inner_circle_radius_dspinbox.setValue(inner_radius)
        
    # slot function: choose save image path
    def handleChooseSaveImagePath(self):
        save_image_folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", os.path.expanduser("~"))
        if save_image_folder_path:
            print("Selected Folder Path: ", save_image_folder_path)
            self.ui.image_path_line.setText(save_image_folder_path)
            self._ring_scene.save_image_folder_path = save_image_folder_path

            # self.label.setText(f"已选择: {folder_path}")
            # self.load_images(folder_path)



# if __name__ == "__main__":
#     app = QApplication([])
#     para_settings = ParaSettings()
#     para_settings.ui.show()
#     app.exec()

    
