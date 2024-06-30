"""
    Внутренности процесса
    Процесс проверяет доступна ли камера, делает снимок и определяет на нем людей
    Не записывает в БД инфу с каждого карда, а только время нахождения на камере человека
"""

from multiprocessing import Process

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
    def __init__(self, id_, conn, **kwargs):
        super().__init__()
        self.id = id_
        self.run = True
        self.camera = Camera('')
        self.comparator = Comparator()
        self.db_helper = kwargs['db_helper']
        self.conn = conn

    # Периодически отправляет свой статус
    def run(self):
        while self.run:
            pass


