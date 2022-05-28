from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QFrame, QSplitter


from widgets.authorization_window import Authorization
from widgets.main_widget import MainWidget
from config import WINDOW_MINIMUM_SIZE


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.auth_window = None
        self.main_widget = MainWidget(self)
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(WINDOW_MINIMUM_SIZE[0], WINDOW_MINIMUM_SIZE[1])
        self.setWindowTitle("PersonalManager")
        self.move(300, 100)
        self.setCentralWidget(self.main_widget)

    def start(self) -> None:
        """ Запускает приложение.

        Сначала запускается авторизация. После удачной авторизации открывается приложение.

        :return None
        """

        self.auth_window = Authorization(self)
        self.auth_window.show()
