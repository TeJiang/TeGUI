"""
This is a small GUI script that allows you to create a dock to fastly preview hyperspectral data
"""

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import numpy as np
import pyqtgraph as pg
from pyqtgraph.console import ConsoleWidget
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtgraph.Qt import QtWidgets
from widget import Ui_Form

# creator defined parameter
TeGUI_version = "0.1.0"

# creat app
app = pg.mkQApp("TeGUI")
win = QtWidgets.QMainWindow()
area = DockArea()
win.setCentralWidget(area)
win.resize(1000, 600)
win.setWindowTitle(f'TeGUI {TeGUI_version}')

## Create docks, place them into the window one at a time.
d1 = Dock("RGB image", size=(300, 300))     ## give this dock the minimum possible size
d2 = Dock("RGB zoom", size=(150, 150))
d3 = Dock("Spectrum", size=(1000, 250))
d4 = Dock("Index", size=(300, 300))
d5 = Dock("Index zoom", size=(150, 150))
d6 = Dock("Reference", size=(100, 300))
d7 = Dock("Switch index", size=(100, 300))

d8 = Dock("Info", size=(1000, 50))

# set position of the dock
area.addDock(d1, 'top')      ## place d1 at left edge of dock area (it will fill the whole space since there are no other docks yet)
area.addDock(d2, 'right', d1)     ## place d2 at right edge of dock area
area.addDock(d4, 'right', d2)
area.addDock(d5, 'bottom', d2)
area.addDock(d7, 'right', d4)
area.addDock(d6, 'left', d1)
area.addDock(d3, 'bottom')## place d3 at bottom edge of d1
area.addDock(d8, 'bottom', d3)

dock_list = [d1, d2, d3, d4, d5, d6, d7]

## Test ability to move docks programatically after they have been placed
# area.moveDock(d3, 'top', d2)     ## move d4 to top edge of d2

## Add widgets into each dock
w1 = pg.LayoutWidget()
widget = QtWidgets.QPushButton("test")
widget2 = QtWidgets.QPushButton("test2")
widget3 = QtWidgets.QPushButton("test3")
widget4 = QtWidgets.QPushButton("test3")
widget5 = QtWidgets.QPushButton("test3")
widget6 = QtWidgets.QPushButton("test3")
widget7 = QtWidgets.QPushButton("test3")
# widget = uic.loadUi("Test_widget_from_pyqtDesigner.ui")
w1.addWidget(widget, row=0, col=0, rowspan=1)
w1.addWidget(widget2, row=1, col=0, rowspan=1)
w1.addWidget(widget3, row=2, col=0, rowspan=1)
w1.addWidget(widget4, row=3, col=0, rowspan=1)
w1.addWidget(widget5, row=4, col=0, rowspan=1)
w1.addWidget(widget6, row=5, col=0, rowspan=1)
w2 = w1.addLayout(row=6, col=0)

widget8 = QtWidgets.QPushButton("tt")
# widget8.setFixedSize(30, 30)
widget9 = QtWidgets.QPushButton("ss")
widget10 = QtWidgets.QPushButton("aa")
w2.addWidget(widget8, row=0, col=1, rowspan=1)
w2.addWidget(widget9, row=0, col=0, rowspan=1)
w2.addWidget(widget10, row=0, col=2, rowspan=1)

d6.addWidget(w1)

RGB_Item = pg.ImageView()
d1.addWidget(RGB_Item)

def print_dock_size():
    for i, dock in enumerate(dock_list):
        print(i, dock.size())

win.show()

if __name__ == '__main__':
    pg.exec()