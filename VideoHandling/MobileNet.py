import tensorflow as tf
import numpy as np
import cv2
from numpy.linalg import norm


# Загрузка изображения и предобработка
def image_load(path):
    image = cv2.imread(path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (224, 224))
    image_array = np.expand_dims(image_resized, axis=0) / 255.0
    return image_array


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = norm(vec1)
    norm_vec2 = norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


# Загрузка модели MobileNetV2
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
                                               include_top=False,
                                               weights='imagenet')

persons = [r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_368.jpg",
           r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_369.jpg",
           r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_370.jpg",
           r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_371.jpg",
           r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_374.jpg",
           r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\faces\seq_1\Screenshot_375.jpg"]


base_model.load_weights("D:\study\Летняя Практика\mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5")

# "D:\study\Летняя Практика\mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5"

pers_images = []
for i in persons:
    pers_images.append(image_load(i))

# Извлечение вектора характеристик
vectors = []
for v in pers_images:
    vectors.append(base_model.predict(v).flatten())

similarity = [[None for _ in range(len(vectors))] for _ in range(len(vectors))]
for j in range(len(vectors)):
    for k in range(len(vectors)):
        similarity[j][k] = cosine_similarity(vectors[j], vectors[k])

# similarity = cosine_similarity(person1_vector, person2_vector)
print("Косинусное сходство между двумя векторами:", similarity)
