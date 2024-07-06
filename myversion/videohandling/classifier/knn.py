from sklearn.neighbors import KNeighborsClassifier
import numpy as np


class VectorClassifier:
    def __init__(self, n_neighbors=5):
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


# Пример использования:
if __name__ == "__main__":
    classifier = VectorClassifier(n_neighbors=3)

    # Добавляем несколько векторов с известными id
    classifier.add_vector([1.2, 2.3, 3.4], 1)
    classifier.add_vector([2.1, 3.2, 4.3], 2)
    classifier.add_vector([0.5, 1.5, 2.5], 1)

    # Классификация новых векторов
    new_vector1 = [1.0, 2.0, 3.0]
    classified_id1 = classifier.classify_vector(new_vector1)
    print(f"Vector {new_vector1} is classified as id {classified_id1}")

    new_vector2 = [2.5, 3.5, 4.5]
    classified_id2 = classifier.classify_vector(new_vector2)
    print(f"Vector {new_vector2} is classified as id {classified_id2}")
