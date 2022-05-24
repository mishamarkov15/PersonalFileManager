import os.path
import eyed3

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QUrl, Qt, QEvent
from PyQt5.QtGui import QPixmap, QBitmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pathlib import Path

from widgets.slider import Slider


class MusicPlayer(QWidget):
    """ Класс быстрого просмотра аудиофайла.

    Позволяет включать/ставить на паузу трек, регулировать громкость и перематывать трек.

    Attributes
    ----------
    audio_picture: Фото обложки трека.
    layout:  Макет.
    slider: Колесо промотки.
    player: Проигрыватель треков.

    Methods
    -------

    """

    mute_icon: QIcon
    pause_icon: QIcon
    play_icon: QIcon
    volume_icon: QIcon

    def __init__(self, parent):
        super(MusicPlayer, self).__init__(parent)
        self.audio_file_name = None
        self.audio_picture = None
        self.layout = None
        self.slider = None
        self.volume_controller = None
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.update_slider)

        self.init_icons()
        self.init_slider()
        self.init_controller()
        self.init_ui()

    def init_icons(self) -> None:
        """ Загружает иконки для данного виджета.

        :return: None
        """

        self.mute_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'mute-volume-button.png'))
        self.pause_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'pause-button.png'))
        self.play_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'play-button.png'))
        self.volume_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'volume-button.png'))

    def init_slider(self) -> None:
        """ Задаёт поведение ползунка.

        Подключает сигнал на изменение текущего момента аудиофайоа и сигнал на перемотку файла.

        :return: None
        """

        self.slider = Slider(Qt.Horizontal)
        self.slider.sld.sliderReleased.connect(self.change_audio_position)

    def init_controller(self) -> None:
        """ Инициализирует слайдер контроля громкости.

        Если пользователь меняет положение слайдера, то меняется громкость трека.

        :return: None
        """

        self.volume_controller = Slider(Qt.Vertical)
        self.volume_controller.sld.setSliderPosition(50)
        self.volume_controller.sld.sliderMoved.connect(self.set_volume)

    def init_ui(self) -> None:
        self.setMinimumSize(100, 100)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        main_vbox = QGridLayout()
        hbox_buttons = QHBoxLayout()
        hbox_image = QHBoxLayout()

        image = QPixmap(os.path.join(os.getcwd(), 'data', 'assets', 'music-note.png'))
        self.audio_picture = QLabel()
        self.audio_picture.setPixmap(image)
        self.audio_picture.setAlignment(Qt.AlignCenter)
        hbox_image.addWidget(self.audio_picture)

        main_vbox.addLayout(hbox_image, 0, 0, 1, 1)
        main_vbox.addLayout(hbox_buttons, 1, 0, 2, 2)

        btn = QPushButton()
        btn.setIcon(self.play_icon)
        btn.clicked.connect(self.play_audio)
        hbox_buttons.addWidget(btn)

        hbox_buttons.addWidget(self.slider)
        hbox_buttons.addWidget(self.volume_controller)

        self.layout.addLayout(main_vbox, 0, 0)

    def set_volume(self) -> None:
        self.player.setVolume(self.volume_controller.sld.sliderPosition())

    def volume_mute(self) -> None:
        self.player.setMuted(not self.player.isMuted())

    def set_audio_picture(self, file_path: os.path) -> None:
        """ Достаёт обложку из метаданных аудиофайла и устанавливает её на виджет.

        :param file_path: Путь к аудиофайлу.
        :return: None
        """

        audiofile = eyed3.load(file_path)

        images = audiofile.tag.images
        qp = QPixmap()
        qp.loadFromData(images[0].image_data)
        qp.scaled(128, 128, Qt.KeepAspectRatio)
        self.audio_picture.setPixmap(qp)

    def play_audio(self, file_path: os.path=None) -> None:
        """ Запускает аудиофайл на прослушивание.

        :param file_path: Полный путь к аудиофайлу.
        :return: None
        """

        full_file_path = file_path if type(file_path) is os.path else \
            os.path.join(os.getcwd(), 'data', 'audio', 'myagi_patron.mp3')

        self.set_audio_picture(full_file_path)

        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.setVolume(50)
        self.player.play()

    def change_audio_position(self):
        self.player.setPosition(self.player.duration() * (self.slider.sld.sliderPosition() / 100))

    def update_slider(self):
        if self.slider.sld.sliderPressed:
            try:
                self.slider.sld.setSliderPosition((self.player.position() / self.player.duration()) * 100)
            except ZeroDivisionError:
                pass
