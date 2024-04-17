from PyQt6 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('MainWindow.ui', self)
        self.plot(
            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20][::-1],
        )
    def plot(self, h, t):
        self.graphwidget.plot(h, t)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()