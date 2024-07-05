import torchreid
import torch
import cv2
import numpy as np
from scipy.spatial.distance import cdist
from torchvision import transforms as T
from PIL import Image

# Загрузка предобученной модели
model = torchreid.models.build_model(
    name='osnet_x1_0',
    num_classes=1000,
    pretrained=True
)
model = model.cpu()
model.eval()


# Функция для извлечения признаков из изображений
def extract_features(model, img_paths):
    # Предобработка изображений
    transform = T.Compose([
        T.Resize((256, 128)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Загрузка изображений и их предобработка
    imgs = []
    for img_path in img_paths:
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Преобразование BGR в RGB
        img = Image.fromarray(img)  # Преобразование NumPy массива в PIL Image
        img = transform(img)  # Применение трансформаций
        imgs.append(img)

    imgs = torch.stack(imgs, dim=0).cpu()

    with torch.no_grad():
        features = model(imgs)

    return features.cpu().numpy()


# Функция для вычисления расстояний между признаками и поиска совпадений
def match_features(features, query_features, threshold=0.5):
    distances = cdist(query_features, features, metric='euclidean')
    matches = []
    for i, dist in enumerate(distances):
        match_idx = np.argmin(dist)
        if dist[match_idx] < threshold:
            matches.append((i, match_idx))
    return matches


# Пример использования функций
cam1_img_paths = [r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_368.jpg']
cam2_img_paths = [r'D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_369.jpg']

cam1_features = extract_features(model, cam1_img_paths)
cam2_features = extract_features(model, cam2_img_paths)

matches = match_features(cam1_features, cam2_features, threshold=0.1)

for match in matches:
    print(f'Cam1 image {cam1_img_paths[match[0]]} matches with Cam2 image {cam2_img_paths[match[1]]}')
