import os
import bcrypt
import cv2
import face_recognition

from time import time

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QLineEdit, QHBoxLayout, \
    QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon


class Authorization(QDialog):
    """ Окно авторизации.

    """

    app_logo: QPixmap

    def __init__(self, parent=None, password=None):
        super(Authorization, self).__init__(parent)
        self.app_logo = QPixmap(os.path.join(os.getcwd(), 'data', 'MainLogo-removebg.png'))
        self.face_img = self.load_face()
        self.face_id = None
        self.auth_button = None
        self.app_name = None
        self.input_password = None
        self.password_label = None
        self.password = password
        self.layout = None
        self.status = False
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'data', 'AppIcon.ico')))
        self.setWindowTitle("Авторизация")

        self.layout = QGridLayout()

        self.app_name = QLabel()
        self.app_name.setPixmap(self.app_logo)
        self.app_name.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.app_name.setObjectName("AppName")
        self.layout.addWidget(self.app_name, 0, 0, 2, 3)

        hbox = QHBoxLayout()

        self.password_label = QLabel("Пароль")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль...")

        hbox.addWidget(self.password_label)
        hbox.addWidget(self.input_password)

        self.layout.addLayout(hbox, 2, 0, 1, 3)

        self.auth_button = QPushButton("Войти")
        self.auth_button.clicked.connect(self.authorize)

        self.face_id = QPushButton("FaceID")
        self.face_id.clicked.connect(self.read_webcam)

        self.layout.addWidget(self.auth_button, 3, 0, 1, 2)
        self.layout.addWidget(self.face_id, 3, 2, 1, 1)

        self.setFocus()
        self.setLayout(self.layout)

    @staticmethod
    def load_face() -> np.array:
        """ Загружает фото человека для обработки. Именно это фото является ключом ко входу в приложение.

        :return: None
        """

        img = cv2.imread(os.path.join(os.getcwd(), 'data', 'faces', 'IMG_9807.JPG'))
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return face_recognition.face_encodings(rgb_img)[0]

    def authorize(self):
        """ Проверяет авторизацию пользователя. В случае удачной авторизации запускает приложение.

        :return: None
        """

        if self.status:
            self.parent().show()
            self.destroy()
        elif len(self.input_password.text()) >= 8:
            password = self.input_password.text().encode('utf-8')
            if bcrypt.checkpw(password,
                              os.environ["PASSWORD"].encode('utf-8')
                              if self.password is None else self.password):
                self.status = True
                self.authorize()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Введите пароль либо воспользуйтесь FaceID.")
            msg.setWindowTitle("Ошибка авторизации.")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.show()

    def read_webcam(self) -> True:
        self.setDisabled(True)

        cap = cv2.VideoCapture(0)

        start_time = time()

        while time() - start_time < 3:
            ret, frame = cap.read()

            tmp_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                tmp_img = face_recognition.face_encodings(tmp_img)[0]
            except IndexError:
                continue

            if face_recognition.compare_faces([self.face_img], tmp_img):
                self.status = True
                break

            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

        self.setDisabled(False)

        if self.status:
            self.authorize()
            return True
        else:
            return False


class PasswordSetup(QDialog):
    """ Класс окна, в котором пользователь создаёт пароль.

    """

    def __init__(self, parent=None) -> None:
        super(PasswordSetup, self).__init__(parent)
        self.create_password_btn = None
        self.layout = None
        self.password_label = None
        self.password_input = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setMinimumSize(300, 300)
        self.layout = QGridLayout(self)

        hbox = QHBoxLayout()

        self.password_label = QLabel("Придумайте пароль")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль...")

        hbox.addWidget(self.password_label)
        hbox.addWidget(self.password_input)

        self.create_password_btn = QPushButton("Подтвердить")
        self.create_password_btn.clicked.connect(self.write_password)

        self.layout.addLayout(hbox, 0, 0)
        self.layout.addWidget(self.create_password_btn, 1, 1)
        self.setLayout(self.layout)

    def write_password(self) -> None:
        """ Записывает пароль в файл, используя хэширование

        :return: None
        """

        password = self.password_input.text()
        if len(password) < 8:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Длина пароля должна быть не менее 8 символов.")
            msg.setWindowTitle("Некорректный ввод")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()
            return

        password = password.encode('utf-8')
        salt = bcrypt.gensalt()

        hash_password = bcrypt.hashpw(password, salt)

        with open('./.env', 'wb') as file:
            file.write(b"PASSWORD=" + bytes(hash_password) + b"\n")

        self.parent().auth(hash_password)
