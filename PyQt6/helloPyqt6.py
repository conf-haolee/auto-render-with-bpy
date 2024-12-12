"""
    测试第一个pyqt 项目
    参考链接： https://www.byhy.net/py/qt/qt_02/
    time: 2024/12/11
    auther: haolee
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit

import sys, os
# app = QApplication([])
app = QApplication(sys.argv)

window = QMainWindow()
window.resize(500, 400)
window.move(300, 310)
window.setWindowTitle('薪资统计')

textEdit = QPlainTextEdit(window)
textEdit.setPlaceholderText("请输入薪资表")
textEdit.move(10,25)
textEdit.resize(300,350)

button = QPushButton('统计', window)
button.move(380,80)

window.show()

app.exec() # PySide6 是 exec 而不是 exec_
