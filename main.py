"""
    Когда все пойдет по пизде, разбить стекло, достать этот скрипт

    Этот скрипт запускает весь бэк, который работает в автомате
    например ProcessManager

    Класс Initializer создает все общие объекты
"""

from CameraNavigationSummerPractic.DBHelper import DBHelper
from CameraNavigationSummerPractic.VideoHandling.ProcessManager import ProcessManager


class Initializer:
    def __init__(self):
        self.db_helper = DBHelper(database='', user='', password='', host='')
        self.process_manager = ProcessManager()


class EntryPoint:
    def __init__(self):
        self.initializer = Initializer()

    def main(self):
        pass


if __name__ == '__main__':
    entry_point = EntryPoint()
    entry_point.main()
