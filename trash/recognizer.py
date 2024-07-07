import torch
from torchreid.reid.utils import FeatureExtractor
import cv2
from torchvision import transforms
from ultralytics import YOLO
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from CameraNavigationSummerPractic.analyzeData.loading_analyzing import TimeValueLogger


class VectorClassifier:
    def __init__(self, n_neighbors=1):
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.X = []  # Здесь будут храниться ваши векторы
        self.y = []  # Здесь будут храниться соответствующие id

    def add_vector(self, vector, vector_id):
        self.X.append(vector)
        self.y.append(vector_id)
        self._retrain_model()

    def _retrain_model(self):
        # Преобразование в numpy массивы для использования в sklearn
        X_train = np.array(self.X)
        y_train = np.array(self.y)
        # Обучение модели
        self.model.fit(X_train, y_train)

    def classify_vector(self, vector):
        # Предсказание id для нового вектора
        vector = np.array(vector).reshape(1, -1)  # Преобразование вектора в нужный формат
        return self.model.predict(vector)[0]

    def del_id(self, id_):
        idx = self.y.index(id_)
        while idx:
            self.y.pop(idx)
            self.X.pop(idx)
            idx = self.y.index(id_)
        self._retrain_model()


class Model:
    def __init__(self):
        self.extractor = FeatureExtractor(
            model_name='osnet_x0_25',
            device='cpu'  # Используйте 'cpu', если нет доступного GPU
        )
        self.preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((256, 128)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def preprocess_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_processed = self.preprocess(image_rgb)
        image_tensor = image_processed.unsqueeze(0)
        return image_tensor.cuda() if torch.cuda.is_available() else image_tensor

    def get_vector(self, image):
        features = self.extractor(image)
        return features[0].detach().cpu().numpy()


class ReIdRecognizer:
    def __init__(self):
        self.yolo = YOLO("../yolofacenet/yolov8n.pt")
        self.model = Model()
        self.knn = VectorClassifier()
        self.persons = []
        self.logger = TimeValueLogger()

    # Распознаем каждого по одному разу на входе
    def entrance_recognize(self, path, name):
        img = cv2.imread(path)
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.yolo.track(img_color, persist=True, show=False)
        # {"preprocess": None, "inference": None, "postprocess": None}
        self.logger.log(results[0].speed)

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
                self.knn.add_vector(vector, name)

    # используем после entrance_recognize на каждом
    def recognize(self, path):
        img = cv2.imread(path)
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.yolo.track(img_color, persist=True, show=False)
        self.logger.log(results[0].speed)
        persons = []
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
                persons.append(class_id)
                self.knn.add_vector(vector, class_id)
        return persons


if __name__ == '__main__':
    recognizer = ReIdRecognizer()
    recognizer.entrance_recognize(r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\myversion\resources\faces\seq_1\Screenshot_368.jpg', 'Jason')
    recognizer.entrance_recognize(
        r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\myversion\resources\photos\1\8.jpg',
        'Nosaj')
    id_ = recognizer.recognize(r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\myversion\resources\faces\seq_1\Screenshot_369.jpg')
    print(id_)
