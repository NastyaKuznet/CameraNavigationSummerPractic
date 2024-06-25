import psycopg2 as ps
import datetime
from db.config import host, user, password, db_name

def GetOneLineFromQuery(query):
    try:
        connection = ps.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def GetAllLinesFromQuery(query):
    try:
        connection = ps.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def Update(update):
    try:
        connection = ps.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(update)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def AddBuilding(address: str):
    Update(f"insert into building (address) values ('{address}'')")

def AddCamera(xPos, yPos, view_angle, view_width, room_id):
    Update(f"""insert into camera (xPos, yPos, view_angle, view_width, room_id)
                 values ('{xPos}', '{yPos}', '{view_angle}', '{view_width}', '{room_id}')""")

def GetCamerasInfoInRoomFromRoomName(name: str):
    GetAllLinesFromQuery('''select  x_pos, y_pos, view_angle, view_width
                         from camera c join room r on r.id = c.room_id
                         where r.name = {name}''')

def AddWall(startX: float, startY: float, endX: float, endY: float, room_id: int):
    Update(f"""insert into wall (x_start, y_start, x_end, y_end, room_id)
                 values ('{startX}', '{startY}', '{endX}', '{endY}', '{room_id}')""")

def GetWallsInfoInRoomFromRoomName(name: str):
    GetAllLinesFromQuery(f'''select  x_start, y_start, , x_end, y_end
                         from wall w join room r on r.id = w.room_id
                         where r.name = {name}''')

def AddRoom(startX: float, startY: float, width: float, height: float,
            buiulding_id: int, floor: str, name: str):
    Update(f"""insert into wall (x_start, y_start, width, height, building_id, floor, name)
                 values ('{startX}', '{startY}', '{width}', '{height}', '{buiulding_id}',
                 '{floor}', '{name}')""")

def GetAllRoomsInfoInBuilding(address: str):
    GetAllLinesFromQuery(f'''select x_start, y_start, width, height, floor, name'
                         from building b join room r on r.building_id = b.id
                         where b.address = {address}''')
