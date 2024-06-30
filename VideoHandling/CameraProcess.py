"""
    Внутренности процесса
    Процесс проверяет доступна ли камера, делает снимок и определяет на нем людей
    Не записывает в БД инфу с каждого карда, а только время нахождения на камере человека
"""
import time
from multiprocessing import Process
import socket
import struct


class Camera:
    def __init__(self, ip):
        self.ip = ip

    def shot(self):
        pass

    def check_connection(self):
        pass


class Person:
    def __init__(self):
        self.vector = []
        self.face_vector = []
        self.x1, self.y1, self.x2, self.y2 = 0.0, 0.0, 0.0, 0.0
        self.time_in = 0
        self.time_out = 0


class Comparator:
    def __init__(self):
        pass

    def compare(self, pers1, pers2) -> bool:
        pass


class CameraProcess(Process):
    def __init__(self, id_, port, **kwargs):
        super().__init__()
        self.id = id_
        self.db_helper = kwargs['db_helper']

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port

        """alv - alive, nsg - no signal on camera, err - errors in process"""
        self.status = 'alv'

    # Периодически отправляет свой статус
    def run(self):
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

