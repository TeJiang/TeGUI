import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDateEdit, QDateTimeEdit, QDial,
    QDoubleSpinBox, QFontComboBox, QLabel, QLCDNumber, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QRadioButton,
    QSlider, QSpinBox, QTimeEdit, QVBoxLayout, QWidget, QCheckBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My App')
        layout = QVBoxLayout()
        widget = QComboBox()
        widget.addItems(['A', 'B', 'C', 'D'])
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()