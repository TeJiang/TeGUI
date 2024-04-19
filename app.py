from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QDateTime
import os


class FolderStructureViewer(QWidget):
    def __init__(self, root_path):
        super().__init__()
        self.root_path = root_path
        self.initUI()

    def initUI(self):
        self.setLayout(QVBoxLayout())
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['Name', 'Size', 'Type', 'Modified'])
        self.populate_tree(self.root_path, self.tree.invisibleRootItem())
        self.tree.expandAll()
        self.layout().addWidget(self.tree)

    def populate_tree(self, path, parent_item):
        for name in sorted(os.listdir(path)):
            full_path = os.path.join(path, name)
            item = QTreeWidgetItem(parent_item, [name])
            self.add_file_details(item, full_path)
            if os.path.isdir(full_path):
                self.populate_tree(full_path, item)
            item.setExpanded(True)

    def add_file_details(self, item, path):
        if os.path.isdir(path):
            item.setText(2, "Folder")
            item.setText(1, "")
        else:
            item.setText(1, f"{os.path.getsize(path)} bytes")
            item.setText(2, os.path.splitext(path)[1] if os.path.splitext(path)[1] else "File")
        mod_time = QDateTime.fromSecsSinceEpoch(os.path.getmtime(path)).toString("yyyy-MM-dd HH:mm:ss")
        item.setText(3, mod_time)
app = QApplication([])
viewer = FolderStructureViewer('/Users/tejiang/Desktop')  # Specify your folder path here
viewer.show()
app.exec()
