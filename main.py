import os
import ctypes
import sys
import bcrypt

from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

from widgets.main_window import MainWindow


def read_env() -> None:
    """ Создаёт файл .env, если нет и считывает его.

    :return: None
    """

    if not os.path.exists('.env'):
        with open('.env', 'wb') as file:
            file.write(b"PASSWORD=\n")

    load_dotenv('.env')


def check_face_id_photo() -> bool:
    """ Проверяет, есть ли faceID фото для входа в приложение.

    :return: True, если таковое имеется, иначе - False.
    """

    path_to_photos = os.path.join(os.getcwd(), 'data', 'faces')
    return os.path.exists(os.path.join(path_to_photos, 'source.jpg'.lower())) or \
           os.path.exists(os.path.join(path_to_photos, 'source.png'.lower()))


def check_prep(path):
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    check_prep(os.path.join(os.getcwd(), '..', '.storage'))
    app = QApplication(sys.argv)
    window = MainWindow()

    read_env()

    if not check_face_id_photo():
        print('Photo is not found.')
    if os.environ['PASSWORD'] == "":
        window.password_window()
    else:
        window.auth()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
