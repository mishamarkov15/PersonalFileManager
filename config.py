import os.path

WINDOW_MINIMUM_SIZE = (1020, 600)


TEXT_FILE_EXTENSIONS = ['txt', 'py', 'cpp', 'md', 'xml', 'js', 'cfg']
AUDIO_FILE_EXTENSIONS = ['mp3']
IMAGE_FILE_EXTENSIONS = ['png', 'jpg', 'bmp', 'jpeg']
VIDEO_FILE_EXTENSIONS = ['mp4', 'avi', 'flv', 'ts', 'mts']

FACE_PHOTO = os.path.join(os.getcwd(), 'data', 'faces', 'source.jpg')

PATH_TO_STORAGE = os.path.abspath(os.path.join(os.getcwd(), '..', '.storage'))
