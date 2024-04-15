import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('My App')
        button = QPushButton('Click Me', self)

        s


app = QApplication(sys.argv)
window = QMainWindow()
window.show()

app.exec()