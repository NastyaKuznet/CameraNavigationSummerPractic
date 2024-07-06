from collections import deque
from CameraNavigationSummerPractic.myversion.general.DBHelper import DBHelper


class Map:
    def __init__(self):
        self.db_helper = DBHelper(database='big_brother', user='postgres', password='1111', host='localhost')
        self.m = 100
        self.n = 100
        """ 
            Список камер. Каждая камера это список из 4х точек
            Камера, Точка зоны видимости 1, точка зоны видимости 2, ближайшая
            точка к центру треугольника
        """
        self.cameras = {}
        self.cam_counter = 0
        """
            Список стен. Каждая стена это две точки в пространстве
        """
        self.walls = {}
        self.walls_counter = 0

        self.graph_lines = []

    def add_wall(self, x1, y1, x2, y2):
        # Здесь должна быть проверка, чтобы рядом с линией всегда были свободные точки
        # Т.е. нельзя поставить линию рядом, если она не начинается из другой линии
        self.walls[self.walls_counter] = [x1, y1, x2, y2]
        self.walls_counter += 1
        self.db_helper.exec(f"""
        insert into wall (id_location, coord_start, coord_end) values (1, point({x1}, {y1}), point({x2}, {y2})))
        """)

    def add_camera(self, camera, field1, field2, ip, type_):
        center = ((camera[0] + field1[0] + field2[0]) / 3, (camera[1] + field1[1] + field2[1]) / 3)
        nearest = int(center[0]), int(center[1])
        self.cameras[self.cam_counter] = [camera, field1, field2, nearest]
        self.cam_counter += 1
        self.db_helper.exec(f"""
        insert into camera (id_location, ip, type_, points) values 
        (1, {ip}, {type_}, %s)
        """, [camera, field1, field2, nearest])

    def graph(self):
        # Строим матрицу. Находим кратчайшие расстояния между всеми точками.
        matrix = self.matrix(self.walls)
        graph = []
        for i in self.cameras:
            for j in self.cameras:
                path = self.bfs_shortest_path(matrix, i[3], j[3])
                # Потом возможен вывод ошибки, если путь найти не удалось
                if path != 0:
                    graph.append(path)
        for i in graph:
            self.db_helper.exec("""
            insert into graph (id_location, points) values (1, %s)
            """, i)

    @staticmethod
    # Строит матрицу из 0 и 1, чтобы понять где мы можем ходить
    def matrix(lines):
        # Определение размеров матрицы
        max_x = max(max(line[0][0], line[1][0]) for line in lines)
        max_y = max(max(line[0][1], line[1][1]) for line in lines)

        # Инициализация матрицы нулями
        maze = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # Пометка ячеек, которые принадлежат линиям, единицами
        for (x1, y1), (x2, y2) in lines:
            if x1 == x2:  # Вертикальная линия
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    maze[y][x1] = 1
            elif y1 == y2:  # Горизонтальная линия
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    maze[y1][x] = 1
            else:  # Диагональная линия
                dx = 1 if x2 > x1 else -1
                dy = 1 if y2 > y1 else -1
                x, y = x1, y1
                while x != x2 + dx and y != y2 + dy:
                    maze[y][x] = 1
                    x += dx
                    y += dy

        return maze

    @staticmethod
    def bfs_shortest_path(maze, start, goal):
        rows, cols = len(maze), len(maze[0])
        queue = deque([(start, [start])])  # очередь для BFS с отслеживанием пути
        visited = set([start])  # множество для отслеживания посещенных ячеек

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # возможные направления движения (вверх, вниз, влево, вправо)

        while queue:
            (x, y), path = queue.popleft()

            # Если достигли цели, возвращаем путь
            if (x, y) == goal:
                return path

            # Проверяем все возможные направления движения
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))

        # Если путь не найден, возвращаем 0
        return 0

# Пример использования
# maze = [
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 0],
#     [0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0]
# ]
#
# start = (0, 0)
# goal = (4, 4)
#
# path = bfs_shortest_path(maze, start, goal)
# print("Путь:", path)
