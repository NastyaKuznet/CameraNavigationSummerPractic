from numpy.linalg import norm
import torch
from torchreid.reid.utils import FeatureExtractor
import numpy as np
import cv2
from torchvision import transforms


class Person:
    def __init__(self, id_):
        self.id = id_
        self.vectors = []
        self.cam = 0  # camera id where person right now
        self.history: {int: [float]} = {}  # camera_id:time

    # Возвращает похожесть от 0 до 1
    @staticmethod
    def compare(vec1, vec2) -> float:
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = norm(vec1)
        norm_vec2 = norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    def now(self, camera, vector):
        # self.history[camera].setdefault(camera, 0).append(time.time())
        self.cam = camera
        self.vectors.append(vector)


class Persons:
    def __init__(self):
        self.persons: [Person] = []
        self.counter = 0

    def add(self, camera, vector):
        new = Person(self.counter)
        self.persons.append(new)
        new.now(camera, vector)
        self.counter += 1


class Model:
    def __init__(self):
        # self.model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
        #                                                include_top=False,
        #                                                weights='imagenet')
        # self.model.\
        # load_weights(r"D:\study\Летняя Практика\mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5")
        # self.model = tf.keras.applications.ResNet50(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
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

