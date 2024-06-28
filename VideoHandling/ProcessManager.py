"""
    Класс ProcessManager, который контролирует процессы
    Например по неоплате сервис обращается к нему и выключает обработку этих камер
    В основном цикле он всегда проверяет запущены ли процессы для клиента

    На каждую камеру отдельный процесс
"""


import mpi4py
from Process import Process


class ProcessManager:
    def __init__(self):
        self.processes = []
        self.__find_all()

    # Если вдруг класс сам умер, при новом запуске он должен найти живые процессы и не создавать новые
    def __find_all(self):
        pass

    def create(self):
        pass

    def kill(self):
        pass

    def info(self):
        pass

    def group(self):
        pass
