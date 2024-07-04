import nltk
from matplotlib import pyplot as plt

nltk.download('punkt')
import sympy as sp
import numpy as np
import Wall as w
class WallBuilder:
    def __init__(self, function: str, frequency: int):
        self.frequency = frequency
        self.function = function

    # startX и startY определяют куда от начала координат(например относительно левого нижнего угла комнаты)
    # надо сдвинуть "стену"
    def CreateWallsFromFunction(self, startX: float, startY: float,
                                startCalculation: float, endCalculation: float):
        func = self.function
        x = sp.symbols('x')
        expr = sp.parse_expr(func)

        x_values = np.linspace(startCalculation + startX, endCalculation + startX, self.frequency).tolist()
        y_values = [(expr.subs(x, xi - startX) + startY) for xi in x_values]

        walls = list()
        for i in range(len(x_values) - 1):
            walls.append(w.Wall(x_values[i], y_values[i], x_values[i + 1], y_values[i + 1]))
        return walls

    def CreateWallFromCoordinates(self, startX: float, startY: float, endX: float, endY: float):
        return w.Wall(startX, startY, endX, endY)



wb = WallBuilder("x**2", 11)
walls = wb.CreateWallsFromFunction(0, 0, 0, 10)
for wall in walls:
    print(wall.startX, wall.startY, wall.endX, wall.endY)

plt.plot([wall.startX for wall in walls], [wall.startY for wall in walls])
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Graph of y = {wb.function}')
plt.show()