from PyQt6 import QtCore, QtGui, QtWidgets
from src.TeGUI.gui.TeGUI_SettingWindow import Ui_SettingWindow
class SettingWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SettingWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)

        self.init_ui()
    def init_ui(self):
        pass