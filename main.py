from TeGUI_MainWindow import Ui_MainWindow
from PyQt6 import QtWidgets
from Setup_TeGUI_MainWindow import MainWindow
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()