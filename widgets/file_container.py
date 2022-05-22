from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5 import QtCore


class FileViewer(QFrame, QWidget):

    def __init__(self, parent=None):
        super(FileViewer, self).__init__(parent)
        self.button_button = None
        self.label_button = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setFrameShape(QFrame.StyledPanel)
        self.setMinimumSize(300, 250)

        grid = QGridLayout(self)
        self.setLayout(grid)

        self.button_button = QPushButton(text="Show Button")
        self.button_button.setObjectName('button_button')
        self.button_button.clicked.connect(self.change_right_widget)
        self.label_button = QPushButton(text="Label Button")
        self.label_button.setObjectName('label_button')
        self.label_button.clicked.connect(self.change_right_widget)

        grid.addWidget(self.button_button, 0, 0)
        grid.addWidget(self.label_button, 0, 1)

    def change_right_widget(self) -> None:
        """Изменяет виджет, расположенный справа"""

        main_widget = self.parent().parent()

        if self.sender().objectName() == 'button_button':
            main_widget.right_top_widget.show_selected_file(1)
        elif self.sender().objectName() == 'label_button':
            main_widget.right_top_widget.show_selected_file(2)
