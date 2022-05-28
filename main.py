import os.path
import cv2
import sys
import face_recognition

from PyQt5.QtWidgets import QApplication

from widgets.main_window import MainWindow


def face_recognize() -> True:
    img = cv2.imread(os.path.join(os.getcwd(), 'data', 'faces', 'IMG_9807.JPG'))
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    img2 = cv2.imread(os.path.join(os.getcwd(), 'data', 'faces', 'IMG_9862.jpeg'))
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

    result = face_recognition.compare_faces([img_encoding], img_encoding2)

    return result


def read_webcam():
    img = cv2.imread(os.path.join(os.getcwd(), 'data', 'faces', 'IMG_9807.JPG'))
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        tmp_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            tmp_img = face_recognition.face_encodings(tmp_img)[0]
        except IndexError:
            continue

        if face_recognition.compare_faces([img_encoding], tmp_img):
            break

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return True


def main():
    if read_webcam():
        print('Успешно')

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
