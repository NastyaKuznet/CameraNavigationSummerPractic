import psycopg2 as ps
import datetime
from config import host, user, password, db_name


# здесь пока берется время из datatime.now()


def exec_query(query, info_message):
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
            print(info_message)
            return cursor.fetchone()[0]
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def exec_query_all(query, info_message):
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
            print(info_message)
            return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def exec_update(update, info_message):
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
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def add_person(link_photo):
    exec_update(f"""insert into test.person (linkphoto, timeInput)
                values ('{link_photo}', '{datetime.datetime.now().isoformat()}')""",
                "[INFO] Person was added")


def add_camera(model, x_central, y_central):
    exec_update(f"""insert into test.camera (model, x_central, y_central)
                 values ('{model}', '{x_central}', '{y_central}')""",
                "[INFO] Camera was added")


def add_photo(id_camera, id_person, link_photo):
    exec_update(f"""insert into test.photo (idcamera, idperson, linkphoto, timephoto)
                 values ('{id_camera}', '{id_person}', 
                 '{link_photo}', '{datetime.datetime.now().isoformat()}')""",
                "[INFO] Photo was added")


def add_blind_line(x1, y1, x2, y2, id_camera1, id_camera2):
    exec_update(f"""insert into test.blindline (x1, y1, x2, y2, idcamera1, idcamera2)
                 values ('{x1}', '{y1}', '{x2}', '{y2}', '{id_camera1}', '{id_camera2}')""",
                "[INFO] Blind line was added")


def get_id_camera(model):
    return exec_query(f"""select id from test.camera as c 
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


def get_trajectory(id_person):
    cameras = get_id_camera_from_photo_by_id_person(id_person)
    central_points = [[camera[0], get_central_points(camera[0])[0]] for camera in cameras]
    blind_lines = []
    for camera in cameras:
        lines = get_blind_line(camera[0])
        if len(lines) != 0 and lines not in blind_lines:
            blind_lines.append(lines)
    return  central_points, blind_lines



if __name__ == "__main__":
    #add_photo(4, 3, 'photo5')
    #print(get_id_camera_from_photo_by_id_person(3))
    #add_blind_line(15, 15, 25, 15, 3, 4)
    print(get_trajectory(3))
