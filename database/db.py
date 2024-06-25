import psycopg2 as ps
import datetime
from database.config import host, user, password, db_name


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


def add_person(link_photo):
    exec_query(f"""insert into test.person (linkphoto, timeInput)
                values ('{link_photo}', '{datetime.datetime.now().isoformat()}')""",
               "[INFO] Person was added")


def add_camera(model, x_central, y_central):
    exec_query(f"""insert into test.camera (model, x_central, y_central)
                 values ('{model}', '{x_central}', '{y_central}')""",
               "[INFO] Camera was added")


def add_photo(id_camera, id_person, link_photo):
    exec_query(f"""insert into test.photo (idcamera, idperson, linkphoto, timephoto)
                 values ('{id_camera}', '{id_person}', 
                 '{link_photo}', '{datetime.datetime.now().isoformat()}')""",
               "[INFO] Photo was added")


def add_blind_line(x1, y1, x2, y2, id_camera1, id_camera2):
    exec_query(f"""insert into test.blindline (x1, y1, x2, y2, idcamera1, idcamera2)
                 values ('{x1}', '{y1}', '{x2}', '{y2}', '{id_camera1}', '{id_camera2}')""",
               "[INFO] Blind line was added")


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

