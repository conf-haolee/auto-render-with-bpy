# import ui.ui_para_settings
from ui.ui_para_settings import ParaSettings

from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow

if __name__ == "__main__":
    app = QApplication([])
    para_settings = ParaSettings()
    para_settings.ui.show()
    app.exec()
