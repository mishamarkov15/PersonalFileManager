from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QGridLayout, QTreeView, QFileSystemModel
from PyQt5.QtCore import Qt, QObject, QEvent, QDir, QSortFilterProxyModel
from PyQt5 import QtCore


from config import WINDOW_MINIMUM_SIZE


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

        if file_name.endswith('.mp3'):
            main_widget.right_top_widget.play_audio(file_path)
        elif file_name.endswith('.txt'):
            print('text_file')
        elif file_name.endswith('.jpg') or file_name.endswith('.png'):
            print('picture')

    def init_ui(self) -> None:
        self.setMinimumSize(WINDOW_MINIMUM_SIZE[0] // 1.5, 250)
        self.setFrameShape(QFrame.StyledPanel)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.file_view)
        self.setLayout(self.layout)

    def change_right_widget(self) -> None:
        """Изменяет виджет, расположенный справа"""

        main_widget = self.parent().parent()

        if self.sender().objectName() == 'button_button':
            main_widget.right_top_widget.show_selected_file(1)
        elif self.sender().objectName() == 'label_button':
            main_widget.right_top_widget.show_selected_file(2)
