from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, \
    QFrame, QSplitter

from widgets.authorization_window import Authorization, PasswordSetup
from widgets.main_widget import MainWidget
from config import WINDOW_MINIMUM_SIZE


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.auth_window = None
        self.pswd_window = None
        self.main_widget = MainWidget(self)
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(WINDOW_MINIMUM_SIZE[0], WINDOW_MINIMUM_SIZE[1])
        self.setWindowTitle("PersonalManager")
        self.move(300, 100)
        self.setCentralWidget(self.main_widget)

    def auth(self, password=None) -> None:
        """ Запускает приложение.

        Сначала запускается авторизация. После удачной авторизации открывается приложение.

        :return None
        """

        if self.pswd_window is not None:
            self.pswd_window.destroy()

        self.auth_window = Authorization(self, password=password)
        self.auth_window.show()

    def password_window(self) -> None:
        """ Запускается, если не указано никакого пароля.

        :return: None
        """

        self.pswd_window = PasswordSetup(self)
        self.pswd_window.show()
