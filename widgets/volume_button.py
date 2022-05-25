from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout

from widgets.slider import Slider


class VolumeController(QWidget):
    """ Виджет контроля громкости. Регулировка громкости появляется при наведении на виджет.

    """

    hover = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(VolumeController, self).__init__(parent)
        self.slider = None
        self.button = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setMaximumHeight(150)

        layout = QVBoxLayout()

        self.slider = Slider(Qt.Vertical)
        self.slider.setMaximumSize(100, 100)
        self.slider.hide()

        self.button = QPushButton()
        self.hover.connect(self.button_hover)

        layout.addSpacing(0)
        layout.addWidget(self.slider)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def button_hover(self, hover) -> None:
        # Выплывающий виджет!
        if hover == 'enterEvent':
            self.slider.show()
        elif hover == 'leaveEvent':
            self.slider.hide()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.hover.emit("enterEvent")

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.hover.emit("leaveEvent")
