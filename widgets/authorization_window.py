import os

import cv2
import sys
import face_recognition

from time import time

import numpy as np
from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, QLineEdit, QHBoxLayout, \
    QDialog


class Authorization(QDialog):
    """ Окно авторизации.

    """

    def __init__(self, parent=None):
        super(Authorization, self).__init__(parent)
        self.face_img = self.load_face()
        self.face_id = None
        self.auth_button = None
        self.app_name = None
        self.input_password = None
        self.password_label = None
        self.layout = None
        self.status = False
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()

        self.app_name = QLabel("Personal Manager")
        self.app_name.setObjectName("AppName")
        self.layout.addWidget(self.app_name, 0, 0)

        hbox = QHBoxLayout()

        self.password_label = QLabel("Пароль")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль...")

        hbox.addWidget(self.password_label)
        hbox.addWidget(self.input_password)

        self.layout.addLayout(hbox, 2, 0)

        self.auth_button = QPushButton("Войти")
        self.auth_button.clicked.connect(self.authorize)

        self.face_id = QPushButton("FaceID")
        self.face_id.clicked.connect(self.read_webcam)

        self.layout.addWidget(self.auth_button, 3, 0)
        self.layout.addWidget(self.face_id, 3, 1)

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

    def read_webcam(self) -> True:
        cap = cv2.VideoCapture(0)

        start_time = time()

        while time() - start_time < 5:
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

        if self.status:
            self.authorize()
            return True
        else:
            return False
