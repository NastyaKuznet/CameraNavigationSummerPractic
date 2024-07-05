""" Запускает и останавливает камеры
    Интерфейс для CameraManager (камеры) это классы Recognizer
 """
import threading

from CameraNavigationSummerPractic.myversion.videohandling.reid.recognizer import *


# Пока только поддерживает всех в запущенном состоянии
class CameraManager:
    def __init__(self, db_helper, reco=ReIdRecognizer):
        self.__db_helper = db_helper
        # self.__server = Server()
        self.reco = reco
        self.cameras: {str: BaseRecognizer} = {}
        self.run = True

    def mainloop(self):
        while self.run:
            self.__db_helper.exec('select id, ip, type_ from camera')
            id_, ip, type_ = self.__db_helper.fetch_one()
            while ip:
                if ip in self.cameras.keys():
                    id_, ip, type_ = self.__db_helper.fetch_one()
                    continue
                new = self.reco(self.__db_helper, id_[0], ip[0], type_)
                new.connect()
                if new.status == 'successful connected':
                    threading.Thread(target=new.mainloop).start()
                self.cameras[ip] = new

                id_, ip, type_ = self.__db_helper.fetch_one()
