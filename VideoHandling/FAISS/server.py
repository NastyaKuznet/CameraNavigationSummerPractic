import numpy as np
import faiss
import pickle
from CameraNavigationSummerPractic.DBHelper import DBHelper


class Vectors:
    def __init__(self, npz=None):
        self.__name_to_vec = {}

        if npz:
            data = np.load(npz)
            embeddex_x = data['arr_0']  # 'embeddex_x'
            Y = data['arr_1']  # Y

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

    def add(self, vect, id_):
        self.__name_to_vec.setdefault(id_, []).append(vect)

    def add_npz(self, npz):
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


class Server:
    def __init__(self, db_helper):
        self.db_helper = db_helper
        self.faiss = Faiss()
        self.vectors = Vectors()
        self.__fill_vectors()

        vecs = np.array(self.vectors.get_vecs())
        self.faiss.train(vecs)
        self.faiss.add(vecs)

    def __fill_vectors(self):
        self.db_helper.exec('select vector, id_person from photo')
        pers = self.db_helper.fetch_one()
        while pers:
            self.vectors.add(pers[0], pers[1])
            pers = self.db_helper.fetch_one()

    # Выбирает самого часто втречаемого, возвращает его id
    def get_id_by_vec(self, vec):
        d, i = self.faiss.search(np.array((vec,)), 5)
        max_ = 0
        for k in set(i[0]):
            if i[0].count(k) > max_:
                max_ = k
        return max_


# Обучение
# Добавление векторов в индекс
# Поиск
if __name__ == '__main__':
    db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
    server = Server(db_helper)

    vector666 = np.random.rand(512)
    id_ = server.get_id_by_vec(vector666)
    print(id_)

    # vectors = Vects("faces_embeddings_done_4classes.npz")
    # vecs = vectors.get_vecs()
    #
    # faiss = Faiss()
    # faiss.train(np.array(vecs))
    # faiss.add(np.array(vecs))
    #
    # id_ = 5
    # print(vectors.vec_to_name(vecs[id_]), '\n')
    # vector = vecs[id_]
    # d, i = faiss.search(np.array((vector,)), 5)
    # for k in i[0]:
    #     print(vectors.vec_to_name(vecs[k]))
