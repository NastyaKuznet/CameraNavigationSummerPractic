import Room as r
class Building:
    def __init__(self, address: str, rooms: list):
        self.rooms = rooms
        self.address = address

    def AddRoom(self, startX: int, startY: int, width: int, length: int,
                 walls: list, cameras: list, floor: int, name: str):
        self.rooms.append(r.Room(startX, startY, width, length, walls, cameras, floor, name))