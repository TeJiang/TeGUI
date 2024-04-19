from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog
from pathlib import Path
from PyQt6.QtCore import QDateTime
import sys
import os
from PyQt6 import QtWidgets
import pyqtgraph as pg
from TeGUI_MainWindow import Ui_MainWindow
from Class_Example_Data import example_data

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.work_path = os.getcwd()

        self.data = example_data()

        self.set_window()
        self.set_RGB_image()
        self.set_RGB_image_zoom()
        self.set_index_image()
        self.set_index_image_zoom()

        self.set_hover()
        self.set_menu()
        self.setup_tree_widget()
    def set_menu(self):
        self.ui.actionSet_Working_path.triggered.connect(self.set_work_path)

    def set_work_path(self):
        dialog = QFileDialog()
        directory = dialog.getExistingDirectory(None, "Select Directory", "")
        if directory:
            self.work_path = directory
            print(f"Selected directory: {directory}")
        else:
            pass

        self.populate_tree(self.work_path, self.ui.treeWidget.invisibleRootItem())
        self.ui.treeWidget.expandAll()

    def pass_work_path(self, path):
        self.work_path = Path(path)
        self.populate_tree(self.work_path, self.ui.treeWidget.invisibleRootItem())
        self.ui.treeWidget.expandAll()

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
        self.ui.widget_RGB_Image_Zoom.hideAxis("bottom")
        self.ui.widget_RGB_Image_Zoom.hideAxis("left")

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
        self.ui.widget_Index_Image_Zoom.getPlotItem().hideAxis("bottom")
        self.ui.widget_Index_Image_Zoom.getPlotItem().hideAxis("left")

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
                self.ui.widget_Spectrum.plot(self.data.wl, self.spectrum, pen=pg.mkPen('w', width=2), clear=True)

        except:
            # TODO: debug here
            print("Thre is problem for imageHoverEvent on")

    def set_spectrum(self):
        ...
    def setup_tree_widget(self):
        self.ui.treeWidget.setHeaderLabels(['Name', 'Type', 'Size'])
        self.populate_tree(self.work_path, self.ui.treeWidget.invisibleRootItem())
        self.ui.treeWidget.expandAll()

        self.ui.lineEdit_search.textChanged.connect(self.search_items)

    def populate_tree(self, path, parent_item):
        for name in sorted(os.listdir(path)):
            full_path = os.path.join(path, name)
            item = QTreeWidgetItem(parent_item, [name])
            self.add_file_details(item, full_path)
            if os.path.isdir(full_path):
                self.populate_tree(full_path, item)
            item.setExpanded(True)
    def search_items(self, text):
        # Function to search and filter items
        text = text.lower()
        keyword_list = text.split()
        self.file_format_list = [".sav", ".txt", ".npy"]
        self.file_format_filter = self.ui.comboBox_search_filter.currentText()
        if self.file_format_filter in self.file_format_list:
            if self.file_format_filter not in keyword_list:
                keyword_list.append(self.ui.comboBox_search_filter.currentText())
        print(keyword_list)

        it = QTreeWidgetItemIterator(self.ui.treeWidget)
        while it.value():
            item = it.value()
            item_text = item.text(0).lower()
            if all(text in item_text for text in keyword_list):
                item.setHidden(False)
                self.show_parents(item)
            else:
                item.setHidden(True)
            it += 1
    def show_parents(self, item):
        # Function to make sure all parent items are visible
        while item.parent():
            item = item.parent()
            item.setHidden(False)

    def add_file_details(self, item, path):
        if os.path.isdir(path):
            item.setText(2, "Folder")
            item.setText(1, "")
        else:
            item.setText(2, f"{os.path.getsize(path)} bytes")
            item.setText(1, os.path.splitext(path)[1] if os.path.splitext(path)[1] else "File")
        # mod_time = QDateTime.fromSecsSinceEpoch(os.path.getmtime(path)).toString("yyyy-MM-dd HH:mm:ss")
        # item.setText(3, mod_time)