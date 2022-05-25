import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap


class ImageViewer(QWidget):
    """ Виджет для быстрого просмотра картинок.

    """

    def __init__(self, parent) -> None:
        super(ImageViewer, self).__init__(parent)
        self.image = None
        self.file_name = None
        self.layout = None
        self.init_ui()

    def init_ui(self) -> None:
        self.layout = QGridLayout(self)

        self.file_name = QLabel("")
        self.layout.addWidget(self.file_name, 0, 2, 1, 1)

        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image, 1, 0, 5, 5)

        self.setLayout(self.layout)

    def set_picture(self, file_path: os.path, file_name: str) -> None:
        pixmap = QPixmap(file_path)
        pixmap.scaled(256, 256)
        self.file_name.setText(file_name)
        self.image.setPixmap(pixmap)
