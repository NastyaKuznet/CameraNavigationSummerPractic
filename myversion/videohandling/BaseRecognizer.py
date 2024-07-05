import cv2
from CameraNavigationSummerPractic.myversion.general.DBHelper import DBHelper
from enum import Enum


class Status(Enum):
    CONNECTING = 'connecting',
    CONNECTED = 'successful connected',
    CONNERR = 'connection error',
    DISCONNECTING = 'disconnecting'
    DISCONERR = 'disconnecting error'
    WORKING = 'working'
    NOVIDEO = 'no video'


class BaseRecognizer:
    def __init__(self, db_helper: DBHelper, id_, ip):
        self.__db_helper = db_helper
        self.id = id_
        self.ip = ip if ip != '0' else 0  # "rtsp://192.168.1.2:9999/h264.sdp"
        self.run = True
        self.status = Status.CONNECTING
        self.camera = None

    def connect(self):
        try:
            self.camera = cv2.VideoCapture(self.ip)
            self.status = Status.CONNECTED
        except Exception:
            self.status = Status.CONNERR

    def mainloop(self):
        pass

    def disconnect(self):
        self.status = Status.DISCONNECTING
        try:
            self.run = False
            self.camera.release()
        except Exception:
            self.status = Status.DISCONERR
