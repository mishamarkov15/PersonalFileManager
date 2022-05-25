import os.path
import eyed3

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, \
    QMessageBox
from PyQt5.QtCore import QUrl, Qt, QEvent
from PyQt5.QtGui import QPixmap, QBitmap, QIcon, QMouseEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pathlib import Path

from widgets.slider import Slider
from widgets.volume_button import VolumeController


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
        self.file_path = None
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
        """ Инициализация графического представления данного виджета.

        Организовано с помощью 1 GridLayout, в который помещены 2 HBoxLayout: 1 для фотографии

        :return:
        """

        self.setMinimumSize(256, 256)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        main_vbox = QGridLayout()
        hbox_buttons = QHBoxLayout()
        hbox_image = QHBoxLayout()

        self.audio_picture = QLabel()
        self.audio_picture.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.audio_picture.setAlignment(Qt.AlignCenter)
        self.audio_picture.setBaseSize(256, 256)
        self.audio_picture.setMaximumSize(256, 256)
        hbox_image.addWidget(self.audio_picture)

        main_vbox.addLayout(hbox_image, 0, 0, 2, 2)
        main_vbox.addLayout(hbox_buttons, 1, 0, 1, 1)

        btn = QPushButton()
        btn.setObjectName('play')
        btn.setIcon(self.play_icon)
        btn.clicked.connect(self.play_audio)
        hbox_buttons.addWidget(btn)

        hbox_buttons.addWidget(self.slider)

        volume_btn = VolumeController()
        volume_btn.slider.sld.setSliderPosition(50)
        volume_btn.slider.sld.sliderMoved.connect(self.set_volume)
        volume_btn.button.setIcon(self.volume_icon)
        volume_btn.button.clicked.connect(self.volume_mute)
        hbox_buttons.addWidget(volume_btn)

        # hbox_buttons.addWidget(self.volume_controller)

        self.layout.addLayout(main_vbox, 0, 0)

    def set_volume(self) -> None:
        """ Устанавливает громкость в соответствии со слайдером.

        :return: None
        """

        self.player.setVolume(self.findChild(VolumeController).slider.sld.sliderPosition())

    def volume_mute(self) -> None:
        """ Убирает звук и меняет иконку кнопки.

        :return: None
        """

        if self.player.isMuted():
            self.findChild(VolumeController).button.setIcon(self.volume_icon)
        else:
            self.findChild(VolumeController).button.setIcon(self.mute_icon)
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
        qp.scaled(256, 256)
        self.audio_picture.setPixmap(qp)
        self.audio_picture.setAlignment(Qt.AlignCenter)

    def play_audio(self, file_path: os.path = None) -> None:
        """ Запускает аудиофайл на прослушивание.

        :param file_path: Полный путь к аудиофайлу.
        :return: None
        """

        full_file_path = file_path if type(file_path) is str else self.file_path

        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        if self.player.media() == content:
            self.pause_media()
            return

        try:
            self.set_audio_picture(full_file_path)
            self.player.setMedia(content)
            self.player.setVolume(10)
            self.findChild(QPushButton, name='play').setIcon(self.play_icon)
            self.file_path = full_file_path
        except TypeError:
            self.show_warning(text="Выберите аудиофайл, чтобы запустить его.")

    def show_warning(self, text: str) -> None:
        """ Показывает предупреждение, если не был выбран аудиофайл, но пользователь попробовал запустить его.

        :param text: текст для отображения.
        :return: None
        """

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)

        msg.setText(text)
        msg.setWindowTitle("Предупреждение")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()

    def pause_media(self) -> None:
        """ Ставит трек на паузу, если он играет, иначе - проигрывает его. Так же устанавливает соответствующие иконки.

        :return: None
        """

        if self.player.state() == 1:
            self.player.pause()
            self.findChild(QPushButton, name='play').setIcon(self.play_icon)
        else:
            self.player.play()
            self.findChild(QPushButton, name='play').setIcon(self.pause_icon)

    def change_audio_position(self) -> None:
        """Меняет точку проигрывания аудиофайла при движении ползунка

        :return: None
        """

        self.player.setPosition(self.player.duration() * (self.slider.sld.sliderPosition() / 100))

    def update_slider(self) -> None:
        """Продвигает ползунок аудиофайла.

        :return: None
        """

        if self.slider.is_available:
            try:
                self.slider.sld.setSliderPosition((self.player.position() / self.player.duration()) * 100)
            except ZeroDivisionError:
                pass
