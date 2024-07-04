import cv2 as cv
from VideoHandling.YOLO_MTCNN_FaceNet.YOLO_MTCNN_FACENET import Recognizer
from VideoHandling.FAISS.server import Server
from keras_facenet import FaceNet
from DBHelper import DBHelper
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class RecognizeFromFile:
    def __init__(self, db_helper):
        self.db_helper = db_helper
        self.server = Server(db_helper)
        self.recognizer = Recognizer(db_helper, self.server)
        self.embedder = FaceNet()
        self.xmtcnn = self.embedder.mtcnn()

    def recognize(self, filename):
        img = cv.imread(filename)
        faces = self.xmtcnn.detect_faces(img)

        recognizer = []
        for k in range(len(faces)):
            x1, y1, w1, h1 = faces[k]['box']
            embedding = self.recognizer.get_embedding(img[y1:h1+y1, x1:x1+w1])
            id_, name = self.recognizer.recognize(embedding)
            recognizer.append(id_)

        return recognizer


if __name__ == '__main__':
    db_helper = DBHelper(database='cam_nav', user='postgres', password='1234', host='localhost')
    generator = RecognizeFromFile(db_helper)
    ids = generator.recognize(r"D:\практика\CameraNavigationSummerPractic\resources\photos\1\1.jpg")

    for i in ids:
        print("id person'a в таблице person", i)
