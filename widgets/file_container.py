from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QGridLayout, QTreeView, QFileSystemModel
from PyQt5.QtCore import Qt, QObject, QEvent, QDir, QSortFilterProxyModel
from PyQt5 import QtCore


from config import WINDOW_MINIMUM_SIZE, AUDIO_FILE_EXTENSIONS, TEXT_FILE_EXTENSIONS,\
    IMAGE_FILE_EXTENSIONS, VIDEO_FILE_EXTENSIONS
from widgets.music_player import MusicPlayer
from widgets.text_file_viewer import TextViewer
from widgets.image_viewer import ImageViewer
from widgets.video_player import VideoPlayer


class FileViewer(QFrame, QWidget):

    def __init__(self, parent=None):
        super(FileViewer, self).__init__(parent)
        self.file_view = None
        self.file_model = None
        self.proxy = None
        self.layout = None

        self.init_file_view()
        self.init_ui()

    def init_file_view(self) -> None:
        self.file_view = QTreeView(self)
        self.file_model = QFileSystemModel(self)
        self.proxy = QSortFilterProxyModel(parent=self, filterRole=QFileSystemModel.FileNameRole)

        self.file_view.clicked.connect(self.on_file_view_clicked)
        self.file_view.setModel(self.proxy)
        self.file_view.setAnimated(True)
        self.file_view.setSortingEnabled(True)
        self.file_view.setIndentation(20)

        self.file_model.setRootPath(QDir.currentPath())

        self.proxy.setSourceModel(self.file_model)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_file_view_clicked(self, index):
        source_index = self.proxy.mapToSource(index)
        index_item = self.file_model.index(source_index.row(), 0, source_index.parent())
        file_name = self.file_model.fileName(index_item)
        file_path = self.file_model.filePath(index_item)

        main_widget = self.parent().parent()

        self.change_right_widget(file_name)

        extension = file_name.split('.')[-1].lower()

        if extension in AUDIO_FILE_EXTENSIONS:
            main_widget.right_top_widget.play_audio(file_path)
        elif extension in TEXT_FILE_EXTENSIONS:
            main_widget.right_top_widget.set_text(file_path, file_name)
        elif extension in IMAGE_FILE_EXTENSIONS:
            main_widget.right_top_widget.set_picture(file_path, file_name)
        elif extension in VIDEO_FILE_EXTENSIONS:
            main_widget.right_top_widget.play_video(file_path)

    def init_ui(self) -> None:
        self.setMinimumSize(WINDOW_MINIMUM_SIZE[0] // 1.5, 250)
        self.setFrameShape(QFrame.StyledPanel)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.file_view)
        self.setLayout(self.layout)

    def change_right_widget(self, file_name: str) -> None:
        """ Изменяет виджет, расположенный справа.

        :param file_name: Имя файла, для которого открывается просмотр. Нужен для расширения.
        :return: None
        """

        main_widget = self.parent().parent()

        extension = file_name.split('.')[-1].lower()

        if extension in AUDIO_FILE_EXTENSIONS:
            main_widget.change_right_top_widget(MusicPlayer)
        elif extension in TEXT_FILE_EXTENSIONS:
            main_widget.change_right_top_widget(TextViewer)
        elif extension in IMAGE_FILE_EXTENSIONS:
            main_widget.change_right_top_widget(ImageViewer)
        elif extension in VIDEO_FILE_EXTENSIONS:
            main_widget.change_right_top_widget(VideoPlayer)
