import random
import random as rnd
import os

import cv2
from ultralytics import YOLO
from CameraNavigationSummerPractic.myversion.videohandling.reid.recognition import Model, Persons
from CameraNavigationSummerPractic.myversion.videohandling.classifier.knn import VectorClassifier


class Generator:
    def __init__(self):
        self.n = 50
        self.m = 50
        self.cameras = 6
        self.photo_dir = '../resources/dataset/'

    def simulation(self):
        n = self.cameras * 0.5
        photos = self._generate_photos()
        cameras = self._generate_cameras()
        times = self._generate_time(n * len(photos))

        data = []
        for i in range(len(photos)):
            for j in range(int(n)):
                data.append((photos[i], cameras[rnd.randint(1, self.cameras)], times.pop(0)))

        return data

    # Фотки должны быть проименованы. Для одного человека одно имя
    def _generate_photos(self):
        persons = os.listdir(self.photo_dir)
        photos = []
        for i in persons:
            photo_path = os.listdir(self.photo_dir + i)
            for j in photo_path:
                photos.append(self.photo_dir + i + '/' + j + '.jpg')

        return photos

    # Считаем, что действуем в пределах одних суток
    def _generate_time(self, n):
        times = []
        for i in range(n):
            hour = rnd.randint(0, 24)
            minute = rnd.randint(0, 60)
            seconds = rnd.randint(0, 60)
            times.append((hour, minute, seconds))

        return times

    def _generate_cameras(self):
        cameras = []
        for i in range(1, self.cameras+1):
            x = random.randint(0, self.n)
            y = random.randint(0, self.m)
            cameras.append((i, (x, y)))

        return cameras


# Генерируем данные
# Берем одну фотку каждого для якобы распознавания на входе
# Затем сортируем по времени сгенерированные данные
# В этом порядке обрабатываем фотки
# Из класса для распознавания берем записи о том, когда кто где появился
# Сравниваем с исходными
class RecognizeData:
    def __init__(self):
        self.generator = Generator()
        self.data = self.generator.simulation()
        self.recognized = []
        self.id_name = {}
        self.yolo = YOLO("../yolofacenet/yolov8n.pt")
        self.model = Model()
        self.persons = Persons()
        self.knn = VectorClassifier()
        self.counter = 0

    def entrance_photos(self):
        persons = os.listdir(self.generator.photo_dir)
        photos = []
        for i in persons:
            photo_path = os.listdir(self.generator.photo_dir + i)
            photo = rnd.choice(photo_path)
            photos.append((i, self.generator.photo_dir + i + '/' + photo + '.jpg'))
        return photos

    def entrance_recognize(self):
        photos = self.entrance_photos()
        for photo in photos:
            img = cv2.imread(photo[1])
            img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
                    self.id_name[self.counter] = photo[0]
                    self.knn.add_vector(vector, self.counter)
                    self.counter += 1
                    self.persons.add(0, vector)

    def sort_photos(self):
        self.data = sorted(self.data, key=lambda x: x[2])

    def recognize(self):
        for dat in self.data:
            photo = dat[0]
            img = cv2.imread(photo)
            img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            id_ = dat[1][0]

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
                    class_id = self.knn.classify_vector(vector)
                    self.recognized.append(class_id)
                    self.knn.add_vector(vector, class_id)

    def evaluate(self):
        cases = []
        for i in range(len(self.data)):
            name = self.data[i][0].split('/')[-2]
            real_name = self.id_name[self.recognized[i]]
            if name == real_name:
                cases.append(1)
            else:
                cases.append(0)
        return sum(cases) / len(cases)


if __name__ == '__main__':
    recogn = RecognizeData()
    recogn.entrance_recognize()
    recogn.sort_photos()
    recogn.recognize()
    evaluation = recogn.evaluate()
