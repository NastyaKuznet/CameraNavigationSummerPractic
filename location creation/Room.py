import Wall as w
import WallBuilder as wb
import Camera as c
class Room:
    def __init__(self, startX: float, startY: float, width: float, height: float,
                 walls: list, cameras: list, floor: int, name: str):
        self.cameras = cameras
        self.floor = floor
        self.name = name
        self.startX = startX
        self.startY = startY
        self.width = width
        self.length = height
        self.walls = walls

    def AddCamera(self, xPos: int, yPos: int, view_angle: int, view_width: int):
        self.cameras.append(c.Camera(xPos, yPos, view_angle, view_width))

    def AddWallFromFunction(self, function: str, frequency: int, startX: float, startY: float,
                            startCalculation, endCalculation):
        if isinstance(startCalculation, float) and isinstance(endCalculation, float):
            self.walls.extend(wb.WallBuilder(function, frequency)
                              .CreateWallsFromFunction(startX, startY, startCalculation, endCalculation))
        else:
            self.walls.extend(wb.WallBuilder(function, frequency)
                              .CreateWallsFromFunction(startX, startY, 0, 10))

    def AddWallFromCoordinates(self, startX, startY, endX, endY):
        self.walls.append(w.Wall(startX, startY, endX, endY))