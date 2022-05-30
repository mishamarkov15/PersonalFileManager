import os.path

from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QSplitter, QPushButton, QLabel, QMessageBox, QDialog, \
    QFileDialog
from PyQt5.QtCore import Qt

from widgets.file_container import FileViewer
from widgets.video_player import VideoPlayer
from config import PATH_TO_STORAGE


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
        self.add_dir_btn = None
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

        self.add_dir_btn = QPushButton("Создать папку")
        self.add_dir_btn.clicked.connect(self.create_dir)

        self.remove_btn = QPushButton("Удалить файл")
        self.remove_btn.clicked.connect(self.remove_file)

        grid.addWidget(self.splitter, 0, 0, 5, 5)
        grid.addWidget(self.add_btn, 5, 0, 1, 1)
        grid.addWidget(self.add_dir_btn, 5, 1, 1, 1)
        grid.addWidget(self.remove_btn, 5, 2, 1, 1)

        self.setLayout(grid)
        self.setFocus()

    def get_current_file_path(self) -> str:
        """ Возвращает путь к файлу.

        :return: str путь к выбранному файлу
        """
        index = self.left_top_widget.file_view.currentIndex()
        index_item = self.left_top_widget.file_model.index(index.row(), 0, index.parent())
        return self.left_top_widget.file_model.filePath(index_item)

    def create_dir(self) -> None:
        """ Создаёт папку в хранилище.

        :return: None
        """

        current_path = self.get_current_file_path()
        if current_path == '':
            current_path = PATH_TO_STORAGE
        elif not os.path.isdir(current_path):
            current_path = os.path.abspath(os.path.join(current_path, '..'))

        new_dirs = [file for file in os.listdir(current_path)
                    if os.path.isdir(os.path.join(current_path, file)) and file.startswith('Новая папка')]

        dir_name = 'Новая папка' + ('' if len(new_dirs) == 0 else f' {len(new_dirs)}')
        if os.path.isdir(current_path):
            os.mkdir(os.path.join(current_path, dir_name))
        else:
            os.mkdir(os.path.abspath(os.path.join(current_path, '..', dir_name)))

    def upload_file(self) -> None:
        """ Загружает файл в хранилище.

        :return: None
        """

        file_name = QFileDialog.getOpenFileName(self.sender().parent(),
                                                'Открыть файл', '/home')[0]

        with open(file_name, 'rb') as file:
            data = file.read()

        with open(os.path.join(self.get_current_file_path(), os.path.basename(file_name)), 'wb') as file:
            file.write(data)

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
