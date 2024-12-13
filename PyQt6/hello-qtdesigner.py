"""
    description: 测试qtdesginer ui 与 后端分离
    time:
    name: haolee 
"""
import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

class ParaSettings(QMainWindow):
    def __init__(self):
        super(ParaSettings, self).__init__()
        ui_file_name = "D:/02 study/cvhao_github/auto-render-with-bpy/ui/para2_settings.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
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

if __name__ == "__main__":
    app = QApplication([])
    para_settings = ParaSettings()
    para_settings.ui.show()
    app.exec()

    
