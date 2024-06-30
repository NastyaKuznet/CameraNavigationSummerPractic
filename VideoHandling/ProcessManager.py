"""
    Класс ProcessManager, который контролирует процессы
    В бесконечном цикле всегда контролирует какие камеры обрабатываются
    Релизует бизнес логику
    Например статус клиента: не оплачено. ProcessManager должен отключить обработку камер

    На каждую камеру отдельный процесс
"""


import struct
import time
import os
import signal

from CameraProcess import CameraProcess
import socket
import configparser


class ProcessBank:
    def __init__(self, port):
        self.processes = {}
        self.port = port

    def create(self, id_, **kwargs):
        p = CameraProcess(id_, self.port, **kwargs)
        self.processes[id_] = (p, 'alive', time.time())
        p.start()

    def kill(self, id_):
        if isinstance(self.processes[id_][0], int):
            os.kill(self.processes[id_][0], signal.SIGTERM)
        else:
            p = self.processes[id_][0]
            p.terminate()
            self.processes.pop(id_)


class ProcessManager:
    def __init__(self, db_helper):
        self.db_helper = db_helper

        config = configparser.ConfigParser()
        config.read('ProcessManager.cfg')
        port = config.getint('DEFAULT', 'Port')

        self.process_bank = ProcessBank(port)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))
        self.socket.listen(10000)

        self.__find_all()

    # Если вдруг класс сам умер, при новом запуске он должен найти живые процессы и не создавать новые
    # Так как пока все работает локально, нет проверки целостности
    def __find_all(self):
        start = time.time()
        while time.time() - start < 20:
            proc_info = self.__status()
            self.process_bank.processes[proc_info[0]] = (proc_info[1], proc_info[2], time.time())

    def __status(self):
        conn, addr = self.socket.accept()
        conn.settimeout(5)
        data = conn.recv(11)
        id_ = struct.unpack('!I', data[0:4])[0]
        pid = struct.unpack('!I', data[4:8])[0]
        status = data[8:11].decode('utf-8', errors='ignore')
        conn.close()
        return id_, pid, status

    def mainloop(self):
        while True:
            # Добавляем новеньких, убиваем всех, кто не заплатил
            self.db_helper.exec("""
                                select id, u.status
                                from camera c
                                join location l on l.id = c.location
                                join user u on u.id = l.user
                                """)

            ids = self.db_helper.fetch_all()
            for id_, status in ids:
                if id_ not in self.process_bank.processes.keys() and status == 'p':
                    self.process_bank.create(id_, db_helper=self.db_helper)
                elif id_ in self.process_bank.processes.keys() and status != 'p':
                    self.process_bank.kill(id_)

            # Обновляем информацию о выживших
            start = time.time()
            while time.time() - start < 30:
                proc_info = self.__status()
                self.process_bank.processes[proc_info[0]][2] = time.time()

            # Если 30 секунд не подает признаков жизни, считаем, что пропал без вести, рожаем нового
            for id_, values in self.process_bank.processes.items():
                if values[2] > 30:
                    self.process_bank.create(id_, db_helper=self.db_helper)
