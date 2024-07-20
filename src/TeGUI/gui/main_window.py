from PyQt6.QtWidgets import QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog, QMainWindow
import pyqtgraph as pg
import os
import numpy as np

from src.TeGUI.gui.TeGUI_MainWindow import Ui_MainWindow
from src.TeGUI.io.io import IO

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.work_path = os.getcwd()

        # Use IO class to load example data
        self.data = IO.load_example_data()

        self.set_window()
        self.set_RGB_image()
        self.set_RGB_image_zoom()
        self.set_index_image()
        self.set_index_image_zoom()
        self.set_spectrum()

        self.set_hover()
        self.set_menu()
        self.setup_tree_widget()
        self.set_splitter()

    def set_menu(self):
        self.ui.actionSet_Working_path.triggered.connect(self.set_work_path)
        self.bool_hide_dockWindow = False
        self.ui.actionHide_Files_Parameter.triggered.connect(self.show_hide_dockWindow)
        self.ui.actionFlip_up_down.triggered.connect(self.flip_data_ud)
        self.ui.actionFlip_left_right.triggered.connect(self.flip_data_lr)
        self.ui.actionClockwise_rotate.triggered.connect(self.rotate_data_cw)
        self.ui.actionAntiClockwise_rotate.triggered.connect(self.rotate_data_acw)

    def flip_data_ud(self):
        # Example flip logic
        self.data.RGB_image = self.data.RGB_image[::-1, :]
        self.update_RGB_image()

    def flip_data_lr(self):
        # Example flip logic
        self.data.RGB_image = self.data.RGB_image[:, ::-1]
        self.update_RGB_image()

    def rotate_data_cw(self):
        # Example rotate logic
        self.data.RGB_image = np.rot90(self.data.RGB_image, -1)
        self.update_RGB_image()

    def rotate_data_acw(self):
        # Example rotate logic
        self.data.RGB_image = np.rot90(self.data.RGB_image, 1)
        self.update_RGB_image()

    def show_hide_dockWindow(self):
        if self.bool_hide_dockWindow:
            self.ui.dockWidget.show()
            self.ui.dockWidget_Files.show()
            self.bool_hide_dockWindow = False
        else:
            self.ui.dockWidget_Files.hide()
            self.ui.dockWidget.hide()
            self.bool_hide_dockWindow = True

    def set_work_path(self):
        dialog = QFileDialog()
        directory = dialog.getExistingDirectory(None, "Select Directory", "")
        if directory:
            self.work_path = directory
            self.populate_tree(self.work_path, self.ui.treeWidget.invisibleRootItem())
            self.ui.treeWidget.expandAll()

    def set_window(self):
        self.window_size = int(self.ui.comboBox_image_roi_size.currentText())
        self.half_window = int((self.window_size - 1) / 2)

    def set_splitter(self):
        initial_size = int(self.ui.splitter_image_spectrum.size().height() / 2)
        self.ui.splitter_image_spectrum.setSizes([initial_size, initial_size])

    def set_RGB_image(self):
        self.RGB_image_Item = pg.ImageItem()
        self.RGB_image_Item.setImage(self.data.RGB_image)
        self.ui.widget_RGB_Image.addItem(self.RGB_image_Item)
        self.ui.widget_RGB_Image.setAspectLocked(lock=True, ratio=1)
        self.ui.widget_RGB_Image.setTitle("RGB image")
        self.init_cross_lines(self.ui.widget_RGB_Image, 'RGB_image')

    def set_index_image(self):
        self.Index_image_Item = pg.ImageItem()
        self.Index_image_Item.setImage(self.data.Index_image)
        self.ui.widget_Index_Image.addItem(self.Index_image_Item)
        self.ui.widget_Index_Image.setAspectLocked(lock=True, ratio=1)
        self.ui.widget_Index_Image.setTitle("Index image")
        self.init_cross_lines(self.ui.widget_Index_Image, 'Index_image')

    def set_RGB_image_zoom(self):
        self.RGB_image_zoom_Item = pg.ImageItem()
        self.RGB_image_zoom_Item.setImage(self.data.RGB_image)
        self.ui.widget_RGB_Image_Zoom.addItem(self.RGB_image_zoom_Item)
        self.ui.widget_RGB_Image_Zoom.hideAxis("bottom")
        self.ui.widget_RGB_Image_Zoom.hideAxis("left")
        self.init_cross_lines(self.ui.widget_RGB_Image_Zoom, 'RGB_image_zoom')

    def set_index_image_zoom(self):
        self.Index_image_zoom_Item = pg.ImageItem()
        self.Index_image_zoom_Item.setImage(self.data.Index_image)
        self.ui.widget_Index_Image_Zoom.addItem(self.Index_image_zoom_Item)
        self.ui.widget_Index_Image_Zoom.getPlotItem().hideAxis("bottom")
        self.ui.widget_Index_Image_Zoom.getPlotItem().hideAxis("left")
        self.init_cross_lines(self.ui.widget_Index_Image_Zoom, 'Index_image_zoom')

    def init_cross_lines(self, widget, name):
        setattr(self, f'vl_{name}', pg.InfiniteLine(angle=90, movable=False))
        setattr(self, f'hl_{name}', pg.InfiniteLine(angle=0, movable=False))
        widget.addItem(getattr(self, f'vl_{name}'), ignoreBounds=True)
        widget.addItem(getattr(self, f'hl_{name}'), ignoreBounds=True)
        setattr(self, f'{name}_ROI', pg.ROI([0, 0], [self.window_size, self.window_size], pen=pg.mkPen('r', width=2), movable=False))
        widget.addItem(getattr(self, f'{name}_ROI'))

    def update_RGB_image(self):
        self.RGB_image_Item.setImage(self.data.RGB_image)

    def set_hover(self):
        self.RGB_image_Item.hoverEvent = self.imageHoverEvent_on
        self.ui.widget_Spectrum.mouseMoveEvent = self.spectrumHoverEvent_On

    def set_spectrum(self):
        self.ui.widget_Spectrum.setTitle("Spectrum")
        self.ui.widget_Spectrum.setLabel("left", "Reflectance")
        self.ui.widget_Spectrum.setLabel("bottom", "Wavelength", units='um')

        self.vl_spectrum = pg.InfiniteLine(angle=90, movable=False)
        self.hl_spectrum = pg.InfiniteLine(angle=0, movable=False)

        self.R_line = pg.InfiniteLine(
            pos=self.data.wl[self.data.rgb_indices[0]],
            angle=90,
            pen=pg.mkPen("r", width=1),
            hoverPen=pg.mkPen("r", width=4),
            movable=True,
        )
        self.G_line = pg.InfiniteLine(
            pos=self.data.wl[self.data.rgb_indices[1]],
            angle=90,
            pen=pg.mkPen("g", width=1),
            hoverPen=pg.mkPen("g", width=4),
            movable=True,
        )
        self.B_line = pg.InfiniteLine(
            pos=self.data.wl[self.data.rgb_indices[2]],
            angle=90,
            pen=pg.mkPen("b", width=1),
            hoverPen=pg.mkPen("b", width=4),
            movable=True,
        )

        self.ui.widget_Spectrum.addItem(self.R_line)
        self.ui.widget_Spectrum.addItem(self.G_line)
        self.ui.widget_Spectrum.addItem(self.B_line)

        self.arrow_spectrum_point = pg.ArrowItem(
            angle=90,
            headLen=5,
            headWidth=5,
            tailWidth=5,
            pen=pg.mkPen("r"),
            brush=pg.mkBrush("r")
        )
    def imageHoverEvent_on(self, event):
        try:
            pos = event.pos()
            ppos = self.RGB_image_Item.mapToParent(pos)
            if (0 <= ppos.x() < self.data.RGB_image.shape[0]) and (0 <= ppos.y() < self.data.RGB_image.shape[1]):
                self.mouse_x, self.mouse_y = int(ppos.x()), int(ppos.y())
                self.ui.widget_RGB_Image.setTitle(f"x: {self.mouse_x}, y: {self.mouse_y}")
                self.ui.widget_Index_Image.setTitle(f"x: {self.mouse_x}, y: {self.mouse_y}")

                # Update cross-line positions and ROI positions
                self.update_cross_lines_and_ROI(self.mouse_x, self.mouse_y)

                # Update zoom image
                self.update_zoom(self.mouse_x, self.mouse_y)

                # Update spectrum
                self.spectrum = self.data.cube[self.mouse_x, self.mouse_y, :]
                self.ui.widget_Spectrum.plot(self.data.wl, self.spectrum, pen=pg.mkPen('w', width=2), clear=True)
                self.add_spectrum_items()

        except Exception as e:
            print(f"Hover Event Error: {e}")

    def update_cross_lines_and_ROI(self, mouse_x, mouse_y):
        for name in ['RGB_image', 'Index_image']:
            getattr(self, f'vl_{name}').setPos(mouse_x)
            getattr(self, f'hl_{name}').setPos(mouse_y)
            getattr(self, f'{name}_ROI').setSize([self.window_size, self.window_size])
            getattr(self, f'{name}_ROI').setPos([mouse_x - self.half_window, mouse_y - self.half_window])

    def update_zoom(self, mouse_x, mouse_y):
        for name in ['RGB_image_zoom', 'Index_image_zoom']:
            getattr(self, f'vl_{name}').setPos(mouse_x)
            getattr(self, f'hl_{name}').setPos(mouse_y)
            getattr(self, f'{name}_ROI').setPos([mouse_x - self.half_window, mouse_y - self.half_window])
            zoom_widget = getattr(self.ui, f'widget_{name}')
            zoom_widget.setXRange(mouse_x - 22, mouse_x + 23)
            zoom_widget.setYRange(mouse_y - 22, mouse_y + 23)

    def add_spectrum_items(self):
        self.ui.widget_Spectrum.addItem(self.vl_spectrum, ignoreBounds=True)
        self.ui.widget_Spectrum.addItem(self.hl_spectrum, ignoreBounds=True)
        self.ui.widget_Spectrum.addItem(self.R_line)
        self.ui.widget_Spectrum.addItem(self.G_line)
        self.ui.widget_Spectrum.addItem(self.B_line)

    def spectrumHoverEvent_On(self, evt):
        pos = evt.position()
        ppos = self.ui.widget_Spectrum.plotItem.vb.mapSceneToView(pos)
        self.closest_wl_pos = int(self.find_wl_pos(ppos.x())[0])
        self.vl_spectrum.setPos(ppos.x())
        self.hl_spectrum.setPos(ppos.y())

        if not any(isinstance(x, pg.ArrowItem) for x in self.ui.widget_Spectrum.items()):
            self.ui.widget_Spectrum.addItem(self.arrow_spectrum_point)

        if hasattr(self, "spectrum"):
            self.arrow_spectrum_point.setPos(self.data.wl[self.closest_wl_pos], self.spectrum[self.closest_wl_pos])
            self.ui.widget_Spectrum.setTitle(
                f"wl: {self.data.wl[self.closest_wl_pos]:.4f}, "
                f"ref: {self.spectrum[self.closest_wl_pos]:.4f}, "
                f"depth: {abs(ppos.y() - self.spectrum[self.closest_wl_pos]):.4f}, "
                f"{(abs(ppos.y() - self.spectrum[self.closest_wl_pos]) / ppos.y() * 100):.1f}%"
            )

    def find_wl_pos(self, pos_x):
        distance_list = [abs(pos_x - x) for x in self.data.wl]
        min_distance = min(distance_list)
        min_pos = [index for index, value in enumerate(distance_list) if value == min_distance]
        return min_pos

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
        text = text.lower()
        keyword_list = text.split()
        self.file_format_list = [".sav", ".txt", ".npy"]
        self.file_format_filter = self.ui.comboBox_search_filter.currentText()
        if self.file_format_filter in self.file_format_list and self.file_format_filter not in keyword_list:
            keyword_list.append(self.file_format_filter)

        it = QTreeWidgetItemIterator(self.ui.treeWidget)
        while it.value():
            item = it.value()
            item_text = item.text(0).lower()
            item.setHidden(not all(keyword in item_text for keyword in keyword_list))
            if not item.isHidden():
                self.show_parents(item)
            it += 1

    def show_parents(self, item):
        while item.parent():
            item = item.parent()
            item.setHidden(False)

    def add_file_details(self, item, path):
        if os.path.isdir(path):
            item.setText(1, "")
            item.setText(2, "Folder")
        else:
            item.setText(1, os.path.splitext(path)[1] if os.path.splitext(path)[1] else "File")
            item.setText(2, f"{os.path.getsize(path)} bytes")