from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QSplitter, QPushButton, QLabel
from PyQt5.QtCore import Qt

from widgets.file_container import FileViewer
from widgets.music_player import MusicPlayer

from config import WINDOW_MINIMUM_SIZE


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
        self.splitter = None
        self.buttons = None
        self.left_top_widget = None
        self.right_top_widget = None
        self.bottom_widget = None
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout(self)

        self.left_top_widget = FileViewer(self)

        tmp_label = QLabel(self)
        tmp_label.setText("Выберите файл для предпросмотра.")
        tmp_label.setAlignment(Qt.AlignCenter)

        self.right_top_widget = tmp_label

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_top_widget)
        self.splitter.addWidget(self.right_top_widget)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([300, 150])

        self.buttons = QPushButton("Hello, world!")

        grid.addWidget(self.splitter, 0, 0)
        grid.addWidget(self.buttons, 1, 0)

        self.setLayout(grid)

    def change_right_top_widget(self, widget) -> None:
        """ Меняет правый виджет

        :param widget:
        :return:
        """

        if type(self.right_top_widget) == widget:
            return

        self.right_top_widget.destroy()
        self.right_top_widget = widget(self)

        self.splitter.replaceWidget(1, self.right_top_widget)
