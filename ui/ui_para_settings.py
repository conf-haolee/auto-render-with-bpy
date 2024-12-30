"""
    description: 测试qtdesginer ui 与 后端分离
    time:
    name: haolee 
"""
import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

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

        # Connect the button click signal to the slot
        self.ui.start_render_btn.clicked.connect(self.handleCalc)

    def handleCalc(self):
        print("Start Render!")

# if __name__ == "__main__":
#     app = QApplication([])
#     para_settings = ParaSettings()
#     para_settings.ui.show()
#     app.exec()

    
