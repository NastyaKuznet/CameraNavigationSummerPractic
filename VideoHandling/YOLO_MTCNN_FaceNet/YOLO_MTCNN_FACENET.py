import threading

import cv2
from ultralytics import YOLO
from keras_facenet import FaceNet
import numpy as np
from CameraNavigationSummerPractic.VideoHandling.FAISS.server import Server
from CameraNavigationSummerPractic.DBHelper import DBHelper


class Recognizer:
    def __init__(self, db_helper, server):
        self.embedder = FaceNet()
        self.server: Server = server
        self.db_helper = db_helper

    def get_embedding(self, img: [[]]) -> list | None:
        try:
            face_img = img.astype('float32')
            face_img = np.expand_dims(face_img, axis=0)
            yhat = self.embedder.embeddings(face_img)  # 512
            return yhat[0]
        except Exception:
            return None

    # Связывается с faiss, высчитывает наиболее часто встречающийся вектор
    def recognize(self, embedding_vec) -> tuple:
        ids = self.server.get_id_by_vec(embedding_vec)
        print(ids)
        names = []
        according = {}
        for id_ in ids:
            self.db_helper.exec(f'select pe.id, pe.name from photo p '
                                f'join person pe on pe.id = p.id_person where p.id = {id_}')
            id_, name = self.db_helper.fetch_one()
            names.append(name)
            according[name] = id_
        names_count = {}
        for i in set(names):
            names_count[i] = 0
        for i in names:
            names_count[i] += 1
        name = max(names_count, key=names_count.get)
        return according[name], name


class YOLORecognizer(Recognizer):
    def __init__(self, db_helper, server, camera, source: int | str = 0):
        super().__init__(db_helper, server)
        self.xmtcnn = self.embedder.mtcnn()
        self.model = YOLO("yolov8n.pt")
        self.video = cv2.VideoCapture(source)  # "rtsp://192.168.1.2:9999/h264.sdp"
        self.id = camera

        # frame_skip = 60  # Количество кадров для пропуска
        # frame_count = 0

    def mainloop(self):
        while True:
            ret, frame = self.video.read()

            if not ret:
                break

            # frame_count += 1
            # if frame_count % (frame_skip + 1) != 0:
            #     continue

            img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.model.track(img_color, persist=True, show=False)

            # 0 is a person
            # print(results[0].boxes.cls.cpu().numpy())  # [          0           0]
            # print(results[0].boxes.id)  # tensor([2., 4.])

            if results[0].boxes:
                classes = results[0].boxes.cls.cpu().numpy()
                boxes = results[0].boxes.xywh
                for clas, box in zip(classes, boxes):
                    if int(clas) != 0:
                        continue
                    x, y, w, h = box
                    cv2.rectangle(img_color, (int(x - w // 2), int(y - h // 2)), (int(x + w // 2), int(y + h // 2)),
                                  (255, 0, 0))
                    faces = self.xmtcnn.detect_faces(
                        img_color[int(y - h // 2):int(y + h // 2), int(x - w // 2):int(x + w // 2)])
                    for k in range(len(faces)):
                        x1, y1, w1, h1 = faces[k]['box']
                        cv2.rectangle(img_color, (x1 + int(x - w // 2), y1 + int(y - h // 2)),
                                      (x1 + int(x - w // 2) + w1, y1 + int(y - h // 2) + h1),
                                      (0, 0, 255))
                        embedding = self.get_embedding(img_color[y1 + int(y - h // 2):y1 + int(y - h // 2) + h1,
                                                       x1 + int(x - w // 2):x1 + int(x - w // 2) + w1])
                        id_, name = self.recognize(embedding)
                        self.db_helper.exec(f'insert into appearance (id_person, id_camera) values ({id_}, {self.id})')
                        if name:
                            cv2.putText(img_color, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                                        cv2.LINE_AA)

            img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)

            # res_plotted = results[0].plot()
            cv2.imshow(f"Tracking_Stream", img_color)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

        self.video.release()
        cv2.destroyAllWindows()


class YOLOWithouShow(Recognizer):
    def __init__(self, db_helper, server, camera, source: int | str = 0):
        super().__init__(db_helper, server)
        self.id = camera
        self.xmtcnn = self.embedder.mtcnn()
        self.model = YOLO("yolov8n.pt")
        self.video = cv2.VideoCapture(source)  # "rtsp://192.168.1.2:9999/h264.sdp"
        self.run = True

        # frame_skip = 60  # Количество кадров для пропуска
        # frame_count = 0

    def mainloop(self):
        while self.run:
            ret, frame = self.video.read()

            if not ret:
                break

            # frame_count += 1
            # if frame_count % (frame_skip + 1) != 0:
            #     continue

            img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = self.model.track(img_color, persist=True, show=False)

            # 0 is a person
            # print(results[0].boxes.cls.cpu().numpy())  # [          0           0]
            # print(results[0].boxes.id)  # tensor([2., 4.])

            if results[0].boxes:
                classes = results[0].boxes.cls.cpu().numpy()
                boxes = results[0].boxes.xywh
                for clas, box in zip(classes, boxes):
                    if int(clas) != 0:
                        continue
                    x, y, w, h = box
                    faces = self.xmtcnn.detect_faces(
                        img_color[int(y - h // 2):int(y + h // 2), int(x - w // 2):int(x + w // 2)])
                    for k in range(len(faces)):
                        x1, y1, w1, h1 = faces[k]['box']

                        embedding = self.get_embedding(img_color[y1 + int(y - h // 2):y1 + int(y - h // 2) + h1,
                                                       x1 + int(x - w // 2):x1 + int(x - w // 2) + w1])
                        id_, name = self.recognize(embedding)
                        self.db_helper.exec(f'insert into appearance (id_person, id_camera) values ({id_}, {self.id})')

        self.video.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
    server = Server(db_helper)
    recognizer1 = YOLORecognizer(db_helper, server, 2)
    recognizer2 = YOLORecognizer(db_helper, server, 1, 'rtsp://192.168.1.2:9999/h264.sdp')
    # recognizer1 = YOLOWithouShow(db_helper, server, 2)  # rtsp://192.168.1.2:9999/h264.sdp'
    # recognizer2 = YOLOWithouShow(db_helper, server, 1, 'rtsp://192.168.1.2:9999/h264.sdp')
    threading.Thread(target=recognizer1.mainloop).start()
    threading.Thread(target=recognizer2.mainloop).start()
