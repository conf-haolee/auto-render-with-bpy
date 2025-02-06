from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QCheckBox, QComboBox, QPushButton
from PySide6.QtCore import QSettings, QDir
'''
    测试参数序列化与反序列化
'''
class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QSettings 保存到文本文件示例")

        # 创建 UI 组件
        self.layout = QVBoxLayout()

        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("输入文本")
        
        self.checkbox = QCheckBox("是否启用", self)

        self.combobox = QComboBox(self)
        self.combobox.addItems(["选项1", "选项2", "选项3"])

        self.save_button = QPushButton("保存参数", self)
        self.load_button = QPushButton("加载参数", self)

        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.load_button)
        self.setLayout(self.layout)

        # 绑定信号槽
        self.save_button.clicked.connect(self.save_settings)
        self.load_button.clicked.connect(self.load_settings)

        # 自动加载设置
        self.load_settings()

    def save_settings(self):
        # 定义文件路径和文件名称
        file_path = "settings.ini"  # 或者指定完整路径，例如 "C:/path/to/settings.ini"

        # 使用 QSettings 保存数据到 INI 文件
        settings = QSettings(file_path, QSettings.IniFormat)
        settings.setValue("line_edit_text", self.line_edit.text())
        settings.setValue("checkbox_state", self.checkbox.isChecked())
        settings.setValue("combobox_index", self.combobox.currentIndex())

    def load_settings(self):
        # 定义文件路径和文件名称
        file_path = "settings.ini"  # 或者指定完整路径

        # 使用 QSettings 从 INI 文件加载数据
        settings = QSettings(file_path, QSettings.IniFormat)
        self.line_edit.setText(settings.value("line_edit_text", ""))
        self.checkbox.setChecked(settings.value("checkbox_state", False, type=bool))
        self.combobox.setCurrentIndex(settings.value("combobox_index", 0, type=int))

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
