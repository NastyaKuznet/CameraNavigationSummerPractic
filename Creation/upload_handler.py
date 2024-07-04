from CameraNavigationSummerPractic.VideoHandling.YOLO_MTCNN_FaceNet.vectors_from_photo import Faceloading
from CameraNavigationSummerPractic.DBHelper import DBHelper
import numpy as np
import os


class UploadHandler:
    def __init__(self, db_helper):
        self.db_helper = db_helper
        self.faceloading = Faceloading(r"C:\Users\user\PycharmProjects\CameraNavigationSummerPractic\resources\faces")

    # Например faces\person_id\number.jpg
    def preprocess(self, person_id, number):
        img = self.faceloading.get_face(person_id, number)
        embeddex_x = self.faceloading.get_embedding(img).tolist()

        print(embeddex_x)
        self.db_helper.exec(f'insert into photo (vector, id_person) values (%s, {person_id})', embeddex_x)


if __name__ == '__main__':
    # Да, нужно каким-то образом передавать id человека, чья это фотка, сохранить ее и выяснить ее номер
    db_helper = DBHelper(database='cam_nav', user='postgres', password='1234', host='localhost')
    upload_handler = UploadHandler(db_helper)
    for dir_ in os.listdir(r"C:\Users\user\PycharmProjects\CameraNavigationSummerPractic\resources\faces"):
        path = r"C:\Users\user\PycharmProjects\CameraNavigationSummerPractic\resources\faces\\" + dir_ + '\\'
        for img_name in os.listdir(path):
            path = path + img_name
            upload_handler.preprocess(dir_, img_name)
