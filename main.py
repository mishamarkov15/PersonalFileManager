import os
import sys
import bcrypt

from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication

from widgets.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    if not os.path.exists('.env'):
        with open('.env', 'wb') as file:
            file.write(b"PASSWORD=\n")

    load_dotenv('.env')

    if os.environ['PASSWORD'] == "":
        window.password_window()
    else:
        window.auth()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
