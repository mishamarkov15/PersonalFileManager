from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QFrame, QSplitter

from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.main_widget = MainWidget(self)
        self.init_ui()
        self.organize_widgets()

    def init_ui(self):
        self.setMinimumSize(640, 640)
        self.setWindowTitle("PersonalManager")
        self.move(300, 100)
        self.setCentralWidget(self.main_widget)

    def init_widget_structure(self) -> None:
        self.splitter = QSplitter(Qt.Horizontal)

        grid = QGridLayout()

        self.top_left_frame = QFrame(self)
        self.top_right_frame = QFrame(self)
        self.bottom_widget = QWidget(self)

        self.splitter.addWidget(self.top_left_frame)
        self.splitter.addWidget(self.top_right_frame)


        self.setCentralWidget(self.splitter)

    def organize_widgets(self):
        pass
