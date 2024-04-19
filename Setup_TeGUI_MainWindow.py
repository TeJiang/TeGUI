from PyQt6 import QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from TeGUI_MainWindow import Ui_MainWindow
from Class_Example_Data import example_data
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.data = example_data()

        self.set_RGB_image()
        self.set_index_image()

        self.set_hover()

    def set_RGB_image(self):
        self.RGB_image_Item = pg.ImageItem()
        self.RGB_image_Item.setImage(self.data.RGB_image)
        self.ui.widget_RGB_Image.addItem(self.RGB_image_Item)

        self.vl_RGB_image = pg.InfiniteLine(angle=90, movable=False)
        self.hl_RGB_image = pg.InfiniteLine(angle= 0, movable=False)
        self.ui.widget_RGB_Image.addItem(self.vl_RGB_image, ignoreBounds=True)
        self.ui.widget_RGB_Image.addItem(self.hl_RGB_image, ignoreBounds=True)

    def set_index_image(self):
        self.Index_image_Item = pg.ImageItem()
        self.Index_image_Item.setImage(self.data.Index_image)
        self.ui.widget_Index_Image.addItem(self.Index_image_Item)

        self.vl_index_image = pg.InfiniteLine(angle=90, movable=False)
        self.hl_index_image = pg.InfiniteLine(angle= 0, movable=False)
        self.ui.widget_Index_Image.addItem(self.vl_index_image, ignoreBounds=True)
        self.ui.widget_Index_Image.addItem(self.hl_index_image, ignoreBounds=True)


    def set_hover(self):
        self.RGB_image_Item.hoverEvent = self.imageHoverEvent_on

    def imageHoverEvent_on(self, event):
        try:
            pos = event.pos()
            ppos = self.RGB_image_Item.mapToParent(pos)
            if (0 <= ppos.x() < self.data.RGB_image.shape[0]) and (0 <= ppos.y() < self.data.RGB_image.shape[1]):
                self.mouse_x, self.mouse_y = int(ppos.x()), int(ppos.y()) # mouse position in not very precise, int value

                self.vl_RGB_image.setPos(ppos.x())
                self.vl_index_image.setPos(ppos.x())
                self.hl_RGB_image.setPos(ppos.y())
                self.hl_index_image.setPos(ppos.y())


                self.spectrum = self.data.cube[self.mouse_x, self.mouse_y, :]
                self.ui.widget_Spectrum.plot(self.data.wl, self.spectrum, pen=pg.mkPen('r', width=1), clear=True)

        except:
            # TODO: debug here
            print("Thre is problem for imageHoverEvent on")

    def set_spectrum(self):
        ...