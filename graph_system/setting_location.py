import numpy as np

# ввод координат левой нижней точки и правой верхней точки поля
field = [[0, 0], [30, 20]]

# ввод координат внутрених стен
  # представление [[x1, y1], [x2, y2]] => [[x1, x2,], [y1, y2]]
walls = [[[10, 10], [10, 20]],
          [[20, 0], [20, 10]]]
for i in range(len(walls)):
  walls[i] = np.array(walls[i]).transpose()

# ввод координат камер
cameras = np.array([[9, 15], [5, 1], [19, 5], [25, 19]]).transpose()

# ввод координат зон камер
selected_fields = [[[0, 10], [10, 20]],
                   [[0, 0], [10, 10]],
                   [[10, 0], [20, 10]],
                   [[20, 10], [30, 20]]]

# ввод координат вход/выход с указанием чем именно является
exits = [[5, 15, "Вход/выход"]]
