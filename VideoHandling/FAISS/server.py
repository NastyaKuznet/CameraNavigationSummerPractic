import time
import numpy as np
import faiss
import pickle


class Vectors:
    def __init__(self, npz):
        data = np.load(npz)
        embeddex_x = data['arr_0']  # 'embeddex_x'
        Y = data['arr_1']  # Y

        self.__name_to_vec = {}
        for i in range(len(Y)):
            self.__name_to_vec.setdefault(Y[i], []).append(embeddex_x[i])

    def get_vecs(self):
        vecs = []
        for i in self.__name_to_vec.values():
            for j in i:
                vecs.append(j)
        return vecs

    def dump(self, path):
        pickle.dump(self.__name_to_vec, path)

    def add(self, npz):
        data = np.load(npz)
        embeddex_x = data[0]
        Y = data[1]

        for i in range(len(Y)):
            self.__name_to_vec.setdefault(Y[i], []).append(embeddex_x[i])

    def vec_to_name(self, vec):
        for name, vec_list in self.__name_to_vec.items():
            for vec1 in vec_list:
                if np.array_equal(vec, vec1):
                    return name


class Faiss:
    def __init__(self, dim=512, k=1):
        dim = dim
        k = k
        quantiser = faiss.IndexFlatL2(dim)  # L2 distance quantiser
        self.__index = faiss.IndexIVFFlat(quantiser, dim, k)

    def train(self, vectors):
        if not self.__index.is_trained:
            self.__index.train(vectors)
        else:
            print("Index is already trained")

    def add(self, vectors):
        if not self.__index.is_trained:
            raise Exception("Index must be trained before adding vectors")
        self.__index.add(vectors)

    def search(self, vectors, n):
        D, I = self.__index.search(vectors, n)
        return D, I


# Обучение
# Добавление векторов в индекс
# Поиск
if __name__ == '__main__':
    vectors = Vectors("/home/tiques/PycharmProjects/CameraNavigation/CameraNavigationSummerPractic/VideoHandling/YOLO+MTCNN+FaceNet/faces_embeddings_done_4classes.npz")
    vecs = vectors.get_vecs()

    faiss = Faiss()
    faiss.train(np.array(vecs))
    faiss.add(np.array(vecs))

    id_ = 10
    print(vectors.vec_to_name(vecs[id_]), '\n')
    vector = vecs[id_]
    d, i = faiss.search(np.array((vector,)), 5)
    for k in i[0]:
        print(vectors.vec_to_name(vecs[k]))
