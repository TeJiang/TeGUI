from PyQt6 import QtWidgets
from Setup_TeGUI_MainWindow import MainWindow
from pathlib import Path
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()

    # set default path
    user_path = Path("/Users/tejiang/Desktop/MicrOmegaGUI/data")
    mainwindow.pass_work_path(path=user_path)

    mainwindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()