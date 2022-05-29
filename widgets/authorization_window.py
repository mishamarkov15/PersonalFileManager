import os
import bcrypt
import cv2
import face_recognition

from time import time

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QLineEdit, QHBoxLayout, \
    QDialog, QMessageBox, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon

from config import FACE_PHOTO


class Authorization(QDialog):
    """ Окно авторизации.

    Attributes
    ----------
    app_logo: Логотип, который отрисовывается по центру окна.
    face_img: Изображения лца, которому разрешен доступ.
    face_id: Кнопка, которая запускает процесс распознавания лица.
    auth_button: Кнопка, которая проверяет пароль на корректность и разрешает доступ к приложению.
    app_label: Область, в которой рисуется app_logo.
    input_password: Поле для ввода пароля.
    password_label: Текст рядом с полем ввода пароля (Текст: Пароль).
    password: Пароль, который передается в конструкторе (необязательный параметр).
    layout: Область, в которой отрисовываются все виджеты.
    status: Статус допуска: если True, то доступ разрешен, в противном случае - нет.

    Methods
    -------


    """

    app_logo: QPixmap

    def __init__(self, parent=None, password=None):
        """ Конструктор окна. Инициализирует логику и графический интерфейс.

        :param parent: Родительский виджет.
        :param password: Пароль (передаётся только в случае первого запуска приложения на компьютере,
                        чтобы всё работало без перезагрузки приложения)
        """

        super(Authorization, self).__init__(parent)
        self.app_logo = QPixmap(os.path.join(os.getcwd(), 'data', 'MainLogo-removebg.png'))
        self.face_img = self.load_face()
        self.face_id = None
        self.auth_button = None
        self.app_label = None
        self.input_password = None
        self.password_label = None
        self.password = password
        self.layout = None
        self.status = False
        self.init_ui()

    def init_ui(self) -> None:
        """ Инициализация графического интерфейса.

        :return: None
        """

        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setWindowFlags((self.windowFlags() & ~Qt.WindowFullscreenButtonHint) | Qt.CustomizeWindowHint)
        self.setWindowIcon(QIcon(os.path.join(os.getcwd(), 'data', 'AppIcon.ico')))
        self.setWindowTitle("Авторизация")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.app_label = QLabel()
        self.app_label.setPixmap(self.app_logo)
        self.app_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.app_label.setObjectName("AppName")
        self.layout.addWidget(self.app_label, 0, 0, 2, 3)

        hbox = QHBoxLayout()

        self.password_label = QLabel("Пароль")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль...")
        self.input_password.textEdited.connect(self.update_auth_button)

        hbox.addWidget(self.password_label)
        hbox.addWidget(self.input_password)

        self.layout.addLayout(hbox, 2, 0, 1, 3)

        self.auth_button = QPushButton("Войти")
        self.auth_button.setDisabled(True)
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

        img = cv2.imread(FACE_PHOTO)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return face_recognition.face_encodings(rgb_img)[0]

    def update_auth_button(self) -> None:
        """ Обновляет состояние кнопки 'войти' в зависимости от введенного текста в поле input_password.

        :return: None
        """

        if len(self.input_password.text()) >= 8:
            self.auth_button.setDisabled(False)
        else:
            self.auth_button.setDisabled(True)

    def authorize(self) -> None:
        """ Проверяет авторизацию пользователя. В случае удачной авторизации запускает приложение.

        Если авторизация не пройдена выводит сообщение об оишбке.

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

    def read_webcam(self) -> bool:
        """ Считывает кадры с веб-камеры и проверяет лицо человека на то, что лежит в папке data/faces.

        :return: True, если авторизация пройдена, иначе - False
        """

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

    Attributes
    ----------
    close_eye: Иконка закрытого глаза.
    open_eye: Иконка открытого глаза.
    show_password_btn: Кнопка, показывающая пароль в поле ввода пароля.
    show_repeat_password_btn: Кнопка, показывающая пароль в поле повтора пароля.
    password_label: Текст (Придумайте пароль).
    password_input: Поле ввода пароля.
    repeat_password_label: Текст (Повторите пароль).
    repeat_password_input: Поле ввода повтора пароля.
    create_password_btn: Кнопка регистрации.
    layout: Область, в которой отрисовываются виджеты.

    Methods
    -------
    init_ui: Инициализация графического интерфейса и подключение логики.
    show_password: Переключение видимости вводимого пароля.
    write_password: Хэширование и запись хэша пароля в файл.

    """

    close_eye: QIcon
    open_eye: QIcon

    def __init__(self, parent=None) -> None:
        """ Конструктор окна регистрации.

        :param parent: родительский виджет.
        """

        super(PasswordSetup, self).__init__(parent)
        self.close_eye = QIcon(os.path.join(os.getcwd(), 'data', 'close-eye.ico'))
        self.open_eye = QIcon(os.path.join(os.getcwd(), 'data', 'open-eye.ico'))
        self.show_password_btn = None
        self.show_repeat_password_btn = None
        self.password_label = None
        self.password_input = None
        self.repeat_password_label = None
        self.repeat_password_input = None
        self.create_password_btn = None
        self.layout = None
        self.init_ui()

    def init_ui(self) -> None:
        """ Инициализирует графичский интерфейс и подключает сигналы.

        :return: None
        """

        self.setMinimumSize(350, 200)
        self.setFocusPolicy(Qt.ClickFocus)
        self.setWindowTitle("Регистрация")
        self.setWindowFlags((self.windowFlags() & ~Qt.WindowFullscreenButtonHint) | Qt.CustomizeWindowHint)
        self.layout = QGridLayout(self)

        hbox1 = QHBoxLayout()

        self.password_label = QLabel("Придумайте пароль")

        self.password_input = QLineEdit()
        self.password_input.setMinimumWidth(150)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль...")

        self.show_password_btn = QPushButton()
        self.show_password_btn.setFixedSize(32, 32)
        self.show_password_btn.setObjectName('MainPasswordLine')
        self.show_password_btn.setIcon(self.close_eye)
        self.show_password_btn.clicked.connect(self.show_password)

        hbox1.addWidget(self.password_label)
        hbox1.addStretch(1)
        hbox1.addWidget(self.password_input)
        hbox1.addStretch(1)
        hbox1.addWidget(self.show_password_btn)

        hbox2 = QHBoxLayout()

        self.repeat_password_label = QLabel("Повторите пароль")

        self.repeat_password_input = QLineEdit()
        self.repeat_password_input.setMinimumWidth(150)
        self.repeat_password_input.setEchoMode(QLineEdit.Password)
        self.repeat_password_input.setPlaceholderText("Повторите пароль...")

        self.show_repeat_password_btn = QPushButton()
        self.show_repeat_password_btn.setFixedSize(32, 32)
        self.show_repeat_password_btn.setObjectName("RepeatPasswordLine")
        self.show_repeat_password_btn.setIcon(self.close_eye)
        self.show_repeat_password_btn.clicked.connect(self.show_password)

        hbox2.addWidget(self.repeat_password_label)
        hbox2.addStretch(1)
        hbox2.addWidget(self.repeat_password_input)
        hbox2.addStretch(1)
        hbox2.addWidget(self.show_repeat_password_btn)

        vbox_for_password = QVBoxLayout()
        vbox_for_password.addLayout(hbox1)
        vbox_for_password.addLayout(hbox2)
        vbox_for_password.addStretch(1)

        self.create_password_btn = QPushButton("Подтвердить")
        self.create_password_btn.clicked.connect(self.write_password)

        self.layout.addLayout(vbox_for_password, 0, 0, 1, 2)
        self.layout.addWidget(self.create_password_btn, 1, 1, 1, 1)
        self.setFocus()
        self.setLayout(self.layout)

    def show_password(self) -> None:
        """ Показывает пароль в полях ввода.

        Меняет иконки на кнопках и видимость текста в соответствующих полях.

        :return: None
        """

        if self.sender().objectName() == "MainPasswordLine":
            if self.password_input.echoMode() == QLineEdit.Password:
                self.password_input.setEchoMode(QLineEdit.Normal)
                self.show_password_btn.setIcon(self.open_eye)
            else:
                self.password_input.setEchoMode(QLineEdit.Password)
                self.show_password_btn.setIcon(self.close_eye)
        else:
            if self.repeat_password_input.echoMode() == QLineEdit.Password:
                self.repeat_password_input.setEchoMode(QLineEdit.Normal)
                self.show_repeat_password_btn.setIcon(self.open_eye)
            else:
                self.repeat_password_input.setEchoMode(QLineEdit.Password)
                self.show_repeat_password_btn.setIcon(self.close_eye)

    def write_password(self) -> None:
        """ Записывает пароль в файл, используя хэширование.

        Проверяет, что длина пароля не менее 8 символов, а также что пароли в двух полях ввода совпадают.
        В случае успеха записывает хэш пароля в .env файл и запускает окно авторизации.

        :return: None
        """

        password = self.password_input.text()
        repeat_password = self.repeat_password_input.text()
        if len(password) < 8:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Длина пароля должна быть не менее 8 символов.")
            msg.setWindowTitle("Некорректный ввод")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()
            return
        elif password != repeat_password:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Пароли должны совпадать")
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
