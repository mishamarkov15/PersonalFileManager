from PyQt5.QtWidgets import QWidget, QFrame
from PyQt5.QtCore import Qt


class ResizableWidget(QFrame):

    def __init__(self, parent=None):
        super(ResizableWidget, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
