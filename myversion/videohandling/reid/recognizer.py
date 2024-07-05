import time
from CameraNavigationSummerPractic.myversion.videohandling.BaseRecognizer import BaseRecognizer, Status
import cv2
from CameraNavigationSummerPractic.myversion.general.DBHelper import DBHelper

from CameraNavigationSummerPractic.myversion.videohandling.reid.recognition import Model, Persons
from ultralytics import YOLO


class ReIdRecognizer(BaseRecognizer):
    def __init__(self, db_helper: DBHelper, id_: int, ip: str, type_: int):
        super().__init__(db_helper, id_, ip)
        self.type = type_  # entry or internal camera; 0 - ent, 1 - int
        self.skip = True if self.ip != 0 else False
        self.yolo = YOLO("../yolofacenet/yolov8n.pt")
        self.model = Model()
        self.persons = Persons()

    def mainloop(self):
        frame_skip = 60  # Количество кадров для пропуска
        frame_count = 0
        while self.run:
            ret, frame = self.camera.read()

            if not ret:
                self.status = Status.NOVIDEO
                time.sleep(1)
                continue

            if self.skip:
                frame_count += 1
                if frame_count % (frame_skip + 1) != 0:
                    continue

            img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.yolo.track(img_color, persist=True, show=False)
            if results[0].boxes:
                classes = results[0].boxes.cls.cpu().numpy()
                boxes = results[0].boxes.xywh
                for clas, box in zip(classes, boxes):
                    if int(clas) != 0:  # 0 is person
                        continue
                    x, y, w, h = box
                    preprocessed = self.model.preprocess(img_color[int(y - h // 2):int(y + h // 2),
                                                         int(x - w // 2):int(x + w // 2)])
                    vector = self.model.get_vector(preprocessed)
                    variety = {}
                    for pers in self.persons.persons:
                        v = pers.compare(pers.vectors[0], vector)
                        variety[v] = pers
                    if len(self.persons.persons) == 0 and self.type == 0:
                        self.persons.add(self.id, vector)
                        print('Новый:', self.persons.counter, 'Камера:', self.id)
                        continue
                    if variety.keys():
                        var = max(variety.keys())
                        if var > 0.7:  # and self.type != 0:
                            variety[var].now(self.id, vector)
                            print('Распознан:', variety[var].id, 'Камера:', self.id, 'Вероятность', var)
                        elif var < 0.7 and self.type == 0:
                            self.persons.add(self.id, vector)
                            print('Новый:', self.persons.counter, 'Камера:', self.id, 'Вероятность', var)

        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    db = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
    # recognizer = ReIdRecognizer(db)
    # recognizer.mainloop()
