import psycopg2 as ps
import datetime
from database.config import host, user, password, db_name, schema_name


# здесь пока берется время из datatime.now() Так что надо будет поменять!!


# метод запроса в целом. его можно юзать, когда надо сделть insert, update, delete
# в обшем когда не нужно ничего возвращать
def exec_query(update, info_message):
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
            print(info_message)
        return cursor
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


# здесь возвращаются все результаты запроса для select
def exec_query_all(query, info_message):
    return exec_query(query, info_message).fetchall()


# здесь возвращается первый результат запроса для select
def exec_query_first(query, info_message):
    return exec_query(query, info_message).fetchone()[0]


def add_user(name):
    exec_query(f"""insert into {schema_name}.users (name)
                          values ('{name}')""",
               "[INFO] User was added")


def add_map(id_user, name, address):
    exec_query(f"""insert into {schema_name}.map (id_user, name, address)
                          values ({id_user}, '{name}', '{address}')""",
               "[INFO] Map was added")


def add_location(name, coord: list, id_map, floor):
    exec_query(f"""insert into {schema_name}.location (name, coord, id_map, floor)
                          values ('{name}', point({coord[0]}, {coord[1]}), {id_map}, {floor})""",
               "[INFO] Location was added")


def add_wall(id_location, coord_start: list, coord_end: list):
    exec_query(f"""insert into {schema_name}.wall (id_location, coord_start, coord_end)
                          values ({id_location}, point({coord_start[0]}, {coord_start[1]}),
                                                 point({coord_end[0]}, {coord_end[1]}))""",
               "[INFO] Wall was added")


def add_camera(id_location, coord: list, angle, width):
    exec_query(f"""insert into {schema_name}.camera (id_location, coord, angle, width)
                 values ({id_location}, point({coord[0]}, {coord[1]}), {angle}, {width})""",
               "[INFO] Camera was added")


def add_blind_line(coord_start: list, coord_end: list, id_camera1, id_camera2):
    exec_query(f"""insert into {schema_name}.blind_line (coord_start, coord_end, id_camera1, id_camera2)
                 values (point({coord_start[0]}, {coord_start[1]}), point({coord_end[0]}, {coord_end[1]}),
                        {id_camera1}, {id_camera2})""",
               "[INFO] Blind line was added")


def add_appearance(id_person, id_camera, data_time: datetime):
    exec_query(f"""insert into {schema_name}.appearance (id_person, id_camera, data_time)
                 values ({id_person}, {id_camera}, {ps.extensions.adapt(data_time)})""",
               "[INFO] Appearance was added")


def add_person(id_photo, name):
    exec_query(f"""insert into {schema_name}.person (id_photo, name)
                 values ({id_photo}, '{name}')""",
               "[INFO] Person was added")


def add_photo(vector: list):
    exec_query(f"""insert into {schema_name}.photo (vector)
                 values (Array[{vector}])""",
               "[INFO] Photo was added")




def get_id_camera(model):
    return exec_query_first(f"""select id from test.camera as c 
                where c.model = '{model}'""",
                            "[INFO] Id camera was received")


def get_id_camera_from_photo_by_id_person(id_person):
    return exec_query_all(f"""select idcamera from test.photo as c
    where c.idperson = '{id_person}'""",
                          "[INFO] Id cameras from photo by id person were received")


def get_central_points(id_camera):
    return exec_query_all(f"""select x_central, y_central  from test.camera as c
    where c.id = '{id_camera}'""",
                          "[INFO] Central points were received")


def get_blind_line(id_camera):
    return exec_query_all(f"""select * from test.blindline as bl
    where bl.idcamera1 = '{id_camera}' or bl.idcamera2 = '{id_camera}'""",
                          "[INFO] Blind line were received")


if __name__ == "__main__":
    pass
    # add_photo(4, 3, 'photo5')

