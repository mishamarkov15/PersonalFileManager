from typing import Union

from PyQt5.QtWidgets import QWidget, QSlider, QGridLayout
from PyQt5.QtCore import Qt


class Slider(QWidget):

    def __init__(self, orientation, parent=None):
        super(Slider, self).__init__(parent)
        self.sld = QSlider(orientation, self)
        grid = QGridLayout(self)
        grid.addWidget(self.sld)
        self.setLayout(grid)

    def update_slider(self, current_position: int, max_position: int) -> None:
        self.sld.setSliderPosition(int(current_position / max_position) * 100)
