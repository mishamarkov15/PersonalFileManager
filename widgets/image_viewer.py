import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap, QImageReader


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
        """Устанавливает картинку в виджет. Если размер картинки меньше размера виджета, то уменьшает её"""

        pixmap = QPixmap(file_path)

        pixmap_size = self.check_size(file_path)

        if pixmap_size.width() > self.image.width() or pixmap_size.height() > self.image.height():
            pixmap = pixmap.scaled(self.image.size(), Qt.KeepAspectRatio)

        self.file_name.setText(file_name)
        self.image.setPixmap(pixmap)

    def repaint(self) -> None:
        """ При изменении размера окна с полноэкранного режима на меньший необходимо перерисовать размер виджета.

        :return: None
        """

        self.setGeometry(self.x(), self.y(), 100, 30)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """ Перерисовывает изображение при изменении размер окна.

        :param a0: Событие изменения размера окна.
        :return: None
        """

        pixmap = self.image.pixmap()

        try:
            if pixmap.width() > self.image.width() or pixmap.height() > self.image.height():
                self.image.setPixmap(pixmap.scaled(self.image.size(), Qt.KeepAspectRatio))
                self.repaint()

        except AttributeError:
            pass

    @staticmethod
    def check_size(file_path: os.path) -> QSize:
        """Узнаёт размер изображения по ширине и высоте"""
        reader = QImageReader(file_path)
        return reader.size()
