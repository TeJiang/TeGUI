import sys

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

        self.set_window()
        self.set_RGB_image()
        self.set_RGB_image_zoom()
        self.set_index_image()
        self.set_index_image_zoom()

        self.set_hover()

    def set_window(self):
        self.window_size = int(self.ui.comboBox_image_roi_size.currentText())
        self.half_window = int((self.window_size - 1) / 2)

    def set_RGB_image(self):
        self.RGB_image_Item = pg.ImageItem()
        self.RGB_image_Item.setImage(self.data.RGB_image)
        self.ui.widget_RGB_Image.addItem(self.RGB_image_Item)

        self.vl_RGB_image = pg.InfiniteLine(angle=90, movable=False)
        self.hl_RGB_image = pg.InfiniteLine(angle= 0, movable=False)
        self.ui.widget_RGB_Image.addItem(self.vl_RGB_image, ignoreBounds=True)
        self.ui.widget_RGB_Image.addItem(self.hl_RGB_image, ignoreBounds=True)

        self.RGB_image_mouse_ROI = pg.ROI([0, 0], [1, 1], pen=pg.mkPen('r', width=2), movable=False)
        self.ui.widget_RGB_Image.addItem(self.RGB_image_mouse_ROI)

    def set_index_image(self):
        self.Index_image_Item = pg.ImageItem()
        self.Index_image_Item.setImage(self.data.Index_image)
        self.ui.widget_Index_Image.addItem(self.Index_image_Item)

        self.vl_index_image = pg.InfiniteLine(angle=90, movable=False)
        self.hl_index_image = pg.InfiniteLine(angle= 0, movable=False)
        self.ui.widget_Index_Image.addItem(self.vl_index_image, ignoreBounds=True)
        self.ui.widget_Index_Image.addItem(self.hl_index_image, ignoreBounds=True)

        self.Index_image_mouse_ROI = pg.ROI([0, 0], [1, 1], pen=pg.mkPen('r', width=2), movable=False)
        self.ui.widget_Index_Image.addItem(self.Index_image_mouse_ROI)
    def set_RGB_image_zoom(self):
        self.RGB_image_zoom_Item = pg.ImageItem()
        self.RGB_image_zoom_Item.setImage(self.data.RGB_image)
        self.ui.widget_RGB_Image_Zoom.addItem(self.RGB_image_zoom_Item)

        self.vl_RGB_image_zoom = pg.InfiniteLine(pos=22.5, angle=90, movable=False)
        self.hl_RGB_image_zoom = pg.InfiniteLine(pos=22.5, angle= 0, movable=False)
        self.ui.widget_RGB_Image_Zoom.addItem(self.vl_RGB_image_zoom)
        self.ui.widget_RGB_Image_Zoom.addItem(self.hl_RGB_image_zoom)
        self.ui.widget_RGB_Image_Zoom.setXRange(0, 45)
        self.ui.widget_RGB_Image_Zoom.setYRange(0, 45)

        self.RGB_image_zoom_ROI = pg.ROI(
            [22.5 - self.half_window - 0.5, 22.5 - self.half_window - 0.5],
            [self.window_size, self.window_size],
            pen="red",
            movable=False,
        )
        self.ui.widget_RGB_Image_Zoom.addItem(self.RGB_image_zoom_ROI)
    def set_index_image_zoom(self):
        self.Index_image_zoom_Item = pg.ImageItem()
        self.Index_image_zoom_Item.setImage(self.data.Index_image)
        self.ui.widget_Index_Image_Zoom.addItem(self.Index_image_zoom_Item)

        self.vl_index_image_zoom = pg.InfiniteLine(pos=22.5, angle=90, movable=False)
        self.hl_index_image_zoom = pg.InfiniteLine(pos=22.5, angle=0, movable=False)
        self.ui.widget_Index_Image_Zoom.addItem(self.vl_index_image_zoom)
        self.ui.widget_Index_Image_Zoom.addItem(self.hl_index_image_zoom)
        self.ui.widget_Index_Image_Zoom.setXRange(0, 45)
        self.ui.widget_Index_Image_Zoom.setYRange(0, 45)

        self.Index_image_zoom_ROI = pg.ROI(
            [22.5 - self.half_window - 0.5, 22.5 - self.half_window - 0.5],
            [self.window_size, self.window_size],
            pen="red",
            movable=False,
        )
        self.ui.widget_Index_Image_Zoom.addItem(self.Index_image_zoom_ROI)

    def set_hover(self):
        self.RGB_image_Item.hoverEvent = self.imageHoverEvent_on

    def imageHoverEvent_on(self, event):
        try:
            pos = event.pos()
            ppos = self.RGB_image_Item.mapToParent(pos)
            if (0 <= ppos.x() < self.data.RGB_image.shape[0]) and (0 <= ppos.y() < self.data.RGB_image.shape[1]):
                self.mouse_x, self.mouse_y = int(ppos.x()), int(ppos.y()) # mouse position in not very precise, int value

                # update cross-line position in RGB image and index image
                self.vl_RGB_image.setPos(ppos.x())
                self.vl_index_image.setPos(ppos.x())
                self.hl_RGB_image.setPos(ppos.y())
                self.hl_index_image.setPos(ppos.y())
                # update mouse ROI position in RGB image and index image
                self.RGB_image_mouse_ROI.setSize([self.window_size, self.window_size])
                self.RGB_image_mouse_ROI.setPos(
                    [
                        self.mouse_x - self.half_window,
                        self.mouse_y - self.half_window,
                    ]
                )
                self.Index_image_mouse_ROI.setSize([self.window_size, self.window_size])
                self.Index_image_mouse_ROI.setPos(
                    [
                        self.mouse_x - self.half_window,
                        self.mouse_y - self.half_window,
                    ]
                )
                # update zoom image
                self.vl_RGB_image_zoom.setPos(ppos.x())
                self.hl_RGB_image_zoom.setPos(ppos.y())
                self.RGB_image_zoom_ROI.setPos(
                    [
                        self.mouse_x - self.half_window,
                        self.mouse_y - self.half_window,
                    ]
                )
                self.ui.widget_RGB_Image_Zoom.setXRange(self.mouse_x-22, self.mouse_x+22+1)
                self.ui.widget_RGB_Image_Zoom.setYRange(self.mouse_y-22, self.mouse_y+22+1)

                self.vl_index_image_zoom.setPos(ppos.x())
                self.hl_index_image_zoom.setPos(ppos.y())
                self.Index_image_zoom_ROI.setPos(
                    [
                        self.mouse_x - self.half_window,
                        self.mouse_y - self.half_window,
                    ]
                )
                self.ui.widget_Index_Image_Zoom.setXRange(self.mouse_x - 22, self.mouse_x + 22 + 1)
                self.ui.widget_Index_Image_Zoom.setYRange(self.mouse_y - 22, self.mouse_y + 22 + 1)

                # update spectrum
                self.spectrum = self.data.cube[self.mouse_x, self.mouse_y, :]
                self.ui.widget_Spectrum.plot(self.data.wl, self.spectrum, pen=pg.mkPen('r', width=1), clear=True)

        except:
            # TODO: debug here
            print("Thre is problem for imageHoverEvent on")

    def set_spectrum(self):
        ...