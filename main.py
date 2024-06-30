"""
    Когда все пойдет по пизде, разбить стекло, достать этот скрипт

    Этот скрипт запускает весь бэк, который работает в автомате
    например ProcessManager

    Класс Initializer создает все общие объекты
"""
import threading

from CameraNavigationSummerPractic.DBHelper import DBHelper
from CameraNavigationSummerPractic.VideoHandling.ProcessManager import ProcessManager


class Initializer:
    def __init__(self):
        self.db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
        self.process_manager = ProcessManager(self.db_helper)


class EntryPoint:
    def __init__(self):
        self.initializer = Initializer()

    def main(self):
        threading.Thread(target=self.initializer.process_manager.mainloop)


if __name__ == '__main__':
    entry_point = EntryPoint()
    entry_point.main()
