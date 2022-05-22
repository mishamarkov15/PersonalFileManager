from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QLabel, QGridLayout


class Preview(QFrame, QWidget):

    def __init__(self, parent=None):
        super(Preview, self).__init__(parent)
        self.label = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setMinimumSize(300, 250)
        self.setFrameShape(QFrame.StyledPanel)

        grid = QGridLayout(self)
        self.setLayout(grid)

    def show_selected_file(self, file_obj: int) -> None:
        """

        1 - label_1
        2 - label_2

        :param file_obj:
        :return:
        """

        if file_obj == 1:
            self.layout().removeWidget(self.label)
            self.label = QLabel("Просмотр текста")
            self.layout().addWidget(self.label)
        elif file_obj == 2:
            self.layout().removeWidget(self.label)
            self.label = QLabel("Просмотр аудио")
            self.layout().addWidget(self.label)

