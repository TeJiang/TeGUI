from PyQt6 import QtWidgets
from src.TeGUI.gui.main_window import MainWindow
import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()

    # set default path
    # user_path = Path("/Users/tejiang/Desktop/MicrOmegaGUI/data")
    # mainwindow.pass_work_path(path=user_path)

    mainwindow.show()
    # set window title
    mainwindow.setWindowTitle("TeGui 0.1")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()