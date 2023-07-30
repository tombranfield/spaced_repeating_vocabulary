import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic


base_dir = os.path.dirname(__file__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(base_dir, "mainwindow.ui"), self)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
