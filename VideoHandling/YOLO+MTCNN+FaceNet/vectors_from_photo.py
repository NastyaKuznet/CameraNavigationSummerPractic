import os
import numpy as np
import cv2 as cv
from keras_facenet import FaceNet


# Каждой фотке будет проставлен label в соответствии с названием подпапки, где она находилась
class Faceloading:
    def __init__(self, directory):
        self.directory = directory
        self.target_size = (160, 160)
        self.X = []
        self.Y = []
        self.embedder = FaceNet()
        self.detector = self.embedder.mtcnn()

    def extract_face(self, filename):
        img = cv.imread(filename)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        x, y, w, h = self.detector.detect_faces(img)[0]['box']
        x, y = abs(x), abs(y)
        face = img[y:y+h, x:x+w]
        face_arr = cv.resize(face, self.target_size)
        return face_arr

    def load_faces(self, directory):
        faces = []
        for img_name in os.listdir(directory):
            try:
                path = directory + img_name
                single_face = self.extract_face(path)
                faces.append(single_face)
            except Exception as e:
                pass
        return faces

    def load_classes(self):
        for sub_dir in os.listdir(self.directory):
            path = self.directory + '\\' + sub_dir + '\\'
            faces = self.load_faces(path)
            labels = [sub_dir for _ in range(len(faces))]
            print(f'Loaded successefully: {len(labels)}')
            self.X.extend(faces)
            self.Y.extend(labels)

        return np.asarray(self.X), np.asarray(self.Y)

    def get_embedding(self, face_img):
        face_img = face_img.astype('float32')
        face_img = np.expand_dims(face_img, axis=0)
        yhat = self.embedder.embeddings(face_img)
        return yhat[0]  # (1x1x512)


if __name__ == '__main__':
    faceloading = Faceloading(r"D:\Python\face_recognition\resources\faces")
    X, Y = faceloading.load_classes()

    embeddex_x = []

    for img in X:
        embeddex_x.append(faceloading.get_embedding(img))

    embeddex_x = np.asarray(embeddex_x)

    np.savez_compressed('faces_embeddings.npz', embeddex_x, Y)

    # # Загрузка данных
    # data = np.load('faces_embeddings_done_4classes.npz')
    #
    # # Извлечение массивов
    # embeddex_x = data['embeddex_x']
    # Y = data['Y']
