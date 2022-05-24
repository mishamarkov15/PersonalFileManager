from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QLabel, QGridLayout, QTreeView, QFileSystemModel


from config import WINDOW_MINIMUM_SIZE


class Preview(QFrame, QWidget):
    """ Виджет просмотра файлов.

    """

    def __init__(self, parent=None):
        super(Preview, self).__init__(parent)
        self.file_view = None
        self.file_model = None

        self.init_file_view()
        self.init_ui()

    def init_file_view(self) -> None:
        self.file_view = QTreeView(self)
        self.file_model = QFileSystemModel(self)

        self.file_view.setModel(self.file_model)
        self.file_model.setRootPath(QDir.currentPath())

    def init_ui(self) -> None:
        self.setMinimumSize(WINDOW_MINIMUM_SIZE[0] // 4, 250)
        self.setFrameShape(QFrame.StyledPanel)

        grid = QGridLayout(self)
        grid.addWidget(self.file_model)
        self.setLayout(grid)
