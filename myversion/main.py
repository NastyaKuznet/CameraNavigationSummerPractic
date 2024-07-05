"""
    Запускает обработку видео с камер
"""
import threading

from CameraNavigationSummerPractic.myversion.general.DBHelper import DBHelper
from CameraNavigationSummerPractic.myversion.videohandling.CameraManager import CameraManager


class Initializer:
    def __init__(self):
        self.db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
        self.camera_manager = CameraManager(self.db_helper)


class EntryPoint:
    def __init__(self):
        self.initializer = Initializer()

    def main(self):
        threading.Thread(target=self.initializer.camera_manager.mainloop)


if __name__ == '__main__':
    entry_point = EntryPoint()
    entry_point.main()
