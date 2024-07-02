from CameraNavigationSummerPractic.VideoHandling.YOLO_MTCNN_FaceNet.YOLO_MTCNN_FACENET import YOLOWithouShow
import threading


# Пока только поддерживает всех в запущенном состоянии
class CameraManager:
    def __init__(self, db_helper, server):
        self.__db_helper = db_helper
        self.__server = server
        self.cameras: {str: YOLOWithouShow} = {}
        self.run = True

    def mainloop(self):
        while self.run:
            self.__db_helper.exec('select id, ip from camera')
            id_, ip = self.__db_helper.fetch_one()
            while ip:
                if ip in self.cameras.keys():
                    id_, ip = self.__db_helper.fetch_one()
                    continue
                new = YOLOWithouShow(self.__db_helper, self.__server, id_[0], ip[0])
                th = threading.Thread(target=new.mainloop)
                self.cameras[ip] = new
                th.start()

                id_, ip = self.__db_helper.fetch_one()

