import os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from widgets.slider import Slider
from widgets.volume_button import VolumeController


class VideoPlayer(QWidget):

    mute_icon: QIcon
    pause_icon: QIcon
    play_icon: QIcon
    volume_icon: QIcon

    def __init__(self, parent=None) -> None:
        super(VideoPlayer, self).__init__(parent)
        self.video_file_name = None
        self.video_widget = None
        self.layout = None
        self.slider = None
        self.volume_controller = None
        self.file_path = None

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.positionChanged.connect(self.update_slider)

        self.init_icons()
        self.init_slider()
        self.init_controller()
        self.init_ui()

    def init_icons(self) -> None:
        self.mute_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'mute-volume-button.png'))
        self.pause_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'pause-button.png'))
        self.play_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'play-button.png'))
        self.volume_icon = QIcon(os.path.join(os.getcwd(), 'data', 'assets', 'qpushbutton', 'volume-button.png'))

    def init_slider(self) -> None:
        self.slider = Slider(Qt.Horizontal)
        self.slider.sld.sliderReleased.connect(self.change_video_position)

    def init_controller(self) -> None:
        self.volume_controller = Slider(Qt.Vertical)
        self.volume_controller.sld.setSliderPosition(50)
        self.volume_controller.sld.sliderMoved.connect(self.set_volume)

    def init_ui(self) -> None:
        self.setMinimumSize(256, 256)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        main_vbox = QGridLayout()
        hbox_buttons = QHBoxLayout()
        hbox_video = QHBoxLayout()

        self.video_widget = QVideoWidget(self)
        hbox_video.addWidget(self.video_widget)

        self.player.setVideoOutput(self.video_widget)

        main_vbox.addLayout(hbox_video, 0, 0, 3, 3)
        main_vbox.addLayout(hbox_buttons, 3, 0, 1, 3)

        btn = QPushButton()
        btn.setObjectName('play')
        btn.setIcon(self.play_icon)
        btn.clicked.connect(self.play_video)
        hbox_buttons.addWidget(btn)

        hbox_buttons.addWidget(self.slider)

        volume_controller = VolumeController()
        volume_controller.slider.sld.setSliderPosition(50)
        volume_controller.slider.sld.sliderMoved.connect(self.set_volume)
        volume_controller.button.setIcon(self.volume_icon)
        volume_controller.button.clicked.connect(self.volume_mute)
        hbox_buttons.addWidget(volume_controller)

        self.layout.addLayout(main_vbox, 0, 0)

    def set_volume(self) -> None:

        self.player.setVolume(self.findChild(VolumeController).slider.sld.sliderPosition())

    def volume_mute(self) -> None:

        if self.player.isMuted():
            self.findChild(VolumeController).button.setIcon(self.volume_icon)
        else:
            self.findChild(VolumeController).button.setIcon(self.mute_icon)
        self.player.setMuted(not self.player.isMuted())

    def play_video(self, file_path: os.path = None) -> None:

        full_file_path = file_path if type(file_path) is str else self.file_path

        url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(url)

        if self.player.media() == content:
            self.pause_media()
            return

        try:
            self.player.setMedia(content)
            self.slider.sld.setSliderPosition(0)
            self.player.setVolume(10)
            self.findChild(QPushButton, name='play').setIcon(self.play_icon)
            self.file_path = full_file_path
        except TypeError:
            pass

    def pause_media(self) -> None:

        if self.player.state() == 1:
            self.player.pause()
            self.slider.is_available = False
            self.findChild(QPushButton, name='play').setIcon(self.play_icon)
        else:
            self.player.play()
            self.slider.is_available = True
            self.findChild(QPushButton, name='play').setIcon(self.pause_icon)

    def change_video_position(self) -> None:

        self.player.setPosition(self.player.duration() * (self.slider.sld.sliderPosition() / 100))

    def update_slider(self) -> None:

        if self.slider.is_available:
            try:
                print('here')
                print(self.player.position(), self.player.duration())
                self.slider.update_slider(self.player.position(), self.player.duration())
            except ZeroDivisionError:
                pass
