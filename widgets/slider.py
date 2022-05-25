from typing import Union

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QSlider, QGridLayout
from PyQt5.QtCore import Qt


class Slider(QWidget):
    """ Виджет слайдера для движения аудио/видео файлов и громкости.

    """

    def __init__(self, orientation, parent=None):
        super(Slider, self).__init__(parent)
        self.sld = QSlider(orientation, self)
        self.sld.sliderPressed.connect(self.block)
        self.sld.sliderReleased.connect(self.unblock)
        grid = QGridLayout(self)
        grid.addWidget(self.sld)
        self.is_available = True  # Для блокировки отрисовки
        self.setLayout(grid)

    def update_slider(self, current_position: int, max_position: int) -> None:
        self.sld.setSliderPosition(int(current_position / max_position) * 100)

    def block(self) -> None:
        self.is_available = False

    def unblock(self) -> None:
        self.is_available = True
