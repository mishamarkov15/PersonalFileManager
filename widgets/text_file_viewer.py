import os
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QGridLayout, QLabel, QTextEdit


class TextViewer(QWidget):
    """ Виджет просмотра текстового файла.

    Считывает данные из файла и выводит их на экран.

    Attributes
    ----------
    text: QPlainText для отображения содержимого файла
    layout: Макет

    """

    def __init__(self, parent) -> None:
        super(TextViewer, self).__init__(parent)
        self.text = None
        self.file_name = None
        self.layout = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setMinimumSize(256, 256)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.file_name = QLabel("")
        self.file_name.setMaximumSize(1000, 20)
        self.layout.addWidget(self.file_name, 0, 2, 1, 1)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text, 1, 0, 5, 5)

    def set_text(self, file_path: os.path, file_name: str) -> None:
        """ Устанавливает текс в виджет.

        :param file_path: Путь к файлу, который открываем.
        :param file_name: Имя файла, чтобы отображать.
        :return: None
        """

        self.file_name.setText(file_name)

        with open(file_path, 'r') as file:
            self.text.setPlainText('\n'.join(file.readlines()))
