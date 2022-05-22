from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QSplitter, QPushButton
from PyQt5.QtCore import Qt

from widgets.file_container import FileViewer
from widgets.file_preview import Preview


class MainWidget(QWidget):
    """ Основной виджет главного окна.

    Состоит из 3 частей:
        1. Левая верхняя - виджет с файлами.
        2. Правая верхняя - виджет с быстрым просмотром файла.
        3. Нижняя - виджет с кнопками.

    Attributes
    ----------
    buttons: Группа с кнопками, расположена в нижней части.
    left_top_widget: QWidget, расположенный в левой верхней части.
    right_top_widget: QWidget, расположенный в правой верхней части.

    """

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.buttons = None
        self.left_top_widget = None
        self.right_top_widget = None
        self.bottom_widget = None
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout(self)

        self.left_top_widget = FileViewer(self)

        self.right_top_widget = Preview(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.left_top_widget)
        splitter.addWidget(self.right_top_widget)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([200, 100])

        self.buttons = QPushButton("Hello, world!")

        grid.addWidget(splitter, 0, 0)
        grid.addWidget(self.buttons, 1, 0)

        self.setLayout(grid)
