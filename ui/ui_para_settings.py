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
from PySide6.QtCore import QFile, QIODevice, Qt, QSettings
sys.path.append("D:/02 study/cvhao_github/auto-render-with-bpy")
from blender_scene import BlenderScene
from detect_real_ring import RealRingDetector

class ParaSettings(QMainWindow):
    def __init__(self):
        super(ParaSettings, self).__init__()
        # use uifile absolute path 
        self._current_dir = os.getcwd()
        ui_file_name = 'ui/para_settings.ui'
        absolute_path = os.path.join(self._current_dir, ui_file_name)
        
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
        icon_path = os.path.join(self._current_dir, 'ui/pic/ringVisionCount_logo3.png')
        self.ui.setWindowIcon(QIcon(icon_path))
        
        # # 创建并显示 SplashScreen
        # splash_path = os.path.join(self._current_dir, 'ui/pic/ringVisionCount_logo1.jpg')
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
        self.ui.save_settings_btn.clicked.connect(self.handleSaveSettings)

        # **程序启动时，自动加载已保存的参数**
        self.load_settings()
    # slot function: start render
    def handleCalc(self):
        print("Start Render!")
        reply = QMessageBox.question(
            self,
            "确认操作",
            "是否保存当前参数？",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if reply == QMessageBox.Yes:
            self.save_settings()  # 先保存参数
            self.handleSaveSettings()
            self._ring_scene.blender_render()
        elif reply == QMessageBox.No:
            self._ring_scene.blender_render()  # 直接运行，不保存
        else:
            print("运行取消")  # 取消操作

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

            # 将计算出的外径和内径赋值给方正场景中
            self._ring_scene.outer_radius = outer_radius
            self._ring_scene.inner_radius = inner_radius
            # 更新UI界面的外径和内径
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
    # slot function: save settings
    def handleSaveSettings(self):
        print("Save Settings!")
        # 设置 圆环的外径和内径
        self._ring_scene.outer_radius = self.ui.outer_circle_radius_dspinbox.value()
        self._ring_scene.inner_radius = self.ui.inner_circle_radius_dspinbox.value()

        # 设置 最大环体数量，渲染图片数量
        self._ring_scene.max_torus_num = self.ui.max_torus_num_spinbox.value()
        self._ring_scene.render_pic_num = self.ui.render_pic_num_spinbox.value()
        # 设置最大形变值
        self._ring_scene.max_deform = self.ui.max_deform_spinbox.value()
        # 设置渲染时 保存图片的文件夹路径
        self._ring_scene.save_image_folder_path = self.ui.image_path_line.text()
        self.save_settings()

    def save_settings(self):
        # 定义文件路径和文件名称
        file_name = 'config/para_settings.ini'
        file_path = os.path.join(self._current_dir, file_name) # 或者指定完整路径，例如 "C:/path/to/settings.ini"

        # 使用 QSettings 保存数据到 INI 文件
        settings = QSettings(file_path, QSettings.IniFormat)
        settings.setValue("real_image_path", self.ui.load_image_path_line.text())
        settings.setValue("outer_circle_radius", self.ui.outer_circle_radius_dspinbox.value())
        settings.setValue("inner_circle_radius", self.ui.inner_circle_radius_dspinbox.value())

        settings.setValue("max_torus_num_spinbox", self.ui.max_torus_num_spinbox.value())
        settings.setValue("max_deform_spinbox", self.ui.max_deform_spinbox.value()) 
        settings.setValue("render_pic_num_spinbox", self.ui.render_pic_num_spinbox.value()) 
        settings.setValue("save_image_path", self.ui.image_path_line.text())

    def load_settings(self):
        # 定义文件路径和文件名称
        file_name = 'config/para_settings.ini'
        file_path = os.path.join(self._current_dir, file_name) # 或者指定完整路径，例如 "C:/path/to/settings.ini"

        # 使用 QSettings 从 INI 文件加载数据
        settings = QSettings(file_path, QSettings.IniFormat)
        self.ui.load_image_path_line.setText(settings.value("real_image_path", ""))
        self.ui.outer_circle_radius_dspinbox.setValue(settings.value("outer_circle_radius", 0.0, type= float))
        self.ui.inner_circle_radius_dspinbox.setValue(settings.value("inner_circle_radius", 0.0 ,type=float))

        self.ui.max_torus_num_spinbox.setValue(settings.value("max_torus_num_spinbox", 0, type=int))
        self.ui.max_deform_spinbox.setValue(settings.value("max_deform_spinbox", 0, type=int))
        self.ui.render_pic_num_spinbox.setValue(settings.value("render_pic_num_spinbox", 0, type=int))
        self.ui.image_path_line.setText(settings.value("save_image_path", ""))

    
