import random
import random as rnd
import os


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
            photo_path = os.listdir(self.photo_dir + i + '.jpg')
            photos.append(photo_path)

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
        for i in range(self.cameras):
            x = random.randint(0, self.n)
            y = random.randint(0, self.m)
            cameras.append((x, y))

        return cameras
