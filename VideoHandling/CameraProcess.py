"""
    Внутренности процесса
    Процесс проверяет доступна ли камера, делает снимок и определяет на нем людей
    Не записывает в БД инфу с каждого карда, а только время нахождения на камере человека
"""
import time
from multiprocessing import Process
import socket
import struct
import cv2
import threading
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Person:
    def __init__(self):
        self.vectors = []
        self.face_vectors = []
        self.imgs = []
        self.time_in = 0
        self.time_out = 0

    def to_vec(self, image, detector):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = detector.detectAndCompute(gray, None)
        return keypoints, descriptors

    @staticmethod
    def is_similar(descriptors1, descriptors2, threshold=0.7):
        if descriptors1 is None or descriptors2 is None:
            return False
        sim = cosine_similarity(descriptors1, descriptors2)
        return np.any(sim > threshold)


class Recognizer:
    def __init__(self, id_, db_helper):
        self.url = self.__url(id_)
        self.db_helper = db_helper
        self.detector = cv2.ORB_create()

    def __url(self, id_):
        self.db_helper.exec(f'select ip from camera where id = {id_}')
        ip = self.db_helper.fetch_one()
        # url = 'https://'
        return ip

    def recognize(self):
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            return 'nsg'

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Детекция людей
            rects, _ = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

            # Отрисовка прямоугольников вокруг людей и векторов
            for (x, y, w, h) in rects:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center = (x + w // 2, y + h // 2)
                cv2.circle(frame, center, 2, (0, 0, 255), 2)

            # Отображение кадра с обведенными людьми и векторами
            cv2.imshow('Detected People', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return 'nsg'


class CameraProcess(Process):
    def __init__(self, id_, port, **kwargs):
        super().__init__()
        self.id = id_
        self.db_helper = kwargs['db_helper']

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

        """alv - alive, nsg - no signal on camera, err - errors in process"""
        self.status = 'alv'

    def run(self):
        threading.Thread(target=self.__send_status)
        recognizer = Recognizer(self.id, self.db_helper)
        while True:
            self.status = recognizer.recognize()

    def __send_status(self):
        while True:
            try:
                self.socket.connect(('localhost', self.port))

                id_ = struct.pack('!I', self.id)
                pid = struct.pack('!I', self.pid)
                status = self.status.encode('utf-8', errors='ignore')

                self.socket.sendall(id_)
                self.socket.sendall(pid)
                self.socket.sendall(status)

                self.socket.close()
            except Exception:
                pass

            time.sleep(10)
