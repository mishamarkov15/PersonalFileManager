from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QSplitter, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

from widgets.file_container import FileViewer
from widgets.video_player import VideoPlayer


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
        self.remove_btn = None
        self.splitter = None
        self.add_btn = None
        self.left_top_widget = None
        self.right_top_widget = None
        self.bottom_widget = None
        self.init_ui()

    def init_ui(self):
        self.setFocusPolicy(Qt.ClickFocus)
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

        self.add_btn = QPushButton("Добавить файл")
        self.add_btn.clicked.connect(self.upload_file)

        self.remove_btn = QPushButton("Удалить файл")
        self.remove_btn.clicked.connect(self.remove_file)

        grid.addWidget(self.splitter, 0, 0, 5, 5)
        grid.addWidget(self.add_btn, 5, 0, 1, 1)
        grid.addWidget(self.remove_btn, 5, 1, 1, 1)

        self.setLayout(grid)
        self.setFocus()

    def upload_file(self) -> None:
        """ Загружает файл в хранилище.

        :return: None
        """

        index = self.left_top_widget.file_view.currentIndex()

        index_item = self.left_top_widget.file_model.index(index.row(), 0, index.parent())
        file_path = self.left_top_widget.file_model.filePath(index_item)
        print(file_path)

    def remove_file(self) -> None:
        """ Удаляет выбранный файл/папку.

        :return: None
        """
        index = self.left_top_widget.file_view.currentIndex()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        if self.left_top_widget.file_model.isDir(index):
            msg.setText("Вы уверены, что хотите удалить выбранную папку?")
        else:
            msg.setText("Вы уверены, что хотите удалить выбранный файл?")
        msg.setWindowTitle("Предупреждение")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.show()
        return_value = msg.exec()

        if return_value == QMessageBox.Yes:
            self.left_top_widget.file_model.remove(index)

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
