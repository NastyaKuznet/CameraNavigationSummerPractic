import cv2 as cv
from CameraNavigationSummerPractic.VideoHandling.YOLO_MTCNN_FaceNet.YOLO_MTCNN_FACENET import Recognizer
from CameraNavigationSummerPractic.VideoHandling.FAISS.server import Server
from keras_facenet import FaceNet
from CameraNavigationSummerPractic.DBHelper import DBHelper


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
    db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
    generator = RecognizeFromFile(db_helper)
    ids = generator.recognize(r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\1\1.jpg")

    for i in ids:
        print("id person'a в таблице person", i)
