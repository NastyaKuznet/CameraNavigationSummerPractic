import torch
from torchreid.reid.utils import FeatureExtractor
import cv2
from torchvision import transforms
from ultralytics import YOLO
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from analyzeData.loading_analyzing import TimeValueLogger
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import pandas as pd


class VectorClassifier:
    def __init__(self, n_neighbors=1):
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)
        self.X = []  # Здесь будут храниться ваши векторы
        self.y = []  # Здесь будут храниться соответствующие id

    def add_vector(self, vector, vector_id):
        print(vector_id)
        self.X.append(vector)
        self.y.append(vector_id)
        self._retrain_model()

    def _retrain_model(self):
        # Преобразование в numpy массивы для использования в sklearn
        X_train = np.array(self.X)
        y_train = np.array(self.y)
        print(y_train)
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

    def plot_vectors(self):
        print(self.y)
        # Применение PCA для снижения размерности до 2D для визуализации
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X)

        # Создание DataFrame для визуализации
        df = pd.DataFrame(X_pca, columns=['Component 1', 'Component 2'])
        df['Vector ID'] = self.y

        # Визуализация
        fig = go.Figure()

        # Добавление точек
        for vector_id in df['Vector ID'].unique():
            cluster_data = df[df['Vector ID'] == vector_id]
            fig.add_trace(go.Scatter(
                x=cluster_data['Component 1'],
                y=cluster_data['Component 2'],
                mode='markers',
                marker=dict(size=10),
                name=f'ID: {vector_id}'
            ))

        # Настройка макета графика
        fig.update_layout(
            title='Vectors Visualization',
            xaxis_title='Component 1',
            yaxis_title='Component 2',
            legend_title='Vector ID'
        )

        # Отображение графика
        fig.show()


class Model:
    def __init__(self):
        self.extractor = FeatureExtractor(
            model_name='osnet_x1_0',
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
        print(path, name)
        img = cv2.imread(path)
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        preprocessed = self.model.preprocess(img_color)
        vector = self.model.get_vector(preprocessed)
        self.knn.add_vector(vector, name)

    # используем после entrance_recognize на каждом
    def recognize(self, path):
        print(path)
        img = cv2.imread(path)
        img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
        img_color = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        persons = []
        preprocessed = self.model.preprocess(img_color)
        vector = self.model.get_vector(preprocessed)
        class_id = self.knn.classify_vector(vector)
        persons.append(class_id)
        self.knn.add_vector(vector, class_id)
        return persons


if __name__ == '__main__':
    reco = ReIdRecognizer()
    reco.entrance_recognize(
        r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\photos\entrance\babka.jpg', 'babka')
    reco.entrance_recognize(
        r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\photos\entrance\Muzhik.jpg',
        'Muzhik')
    reco.entrance_recognize(
        r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\photos\entrance\RedLady.jpg',
        'RedLady')

    res = reco.recognize(r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\sequences\Muzhik\p2 12-09-41 12-10-11.flv228.jpg')
    print(res)

