import psycopg2 as ps
import datetime
from database.config import host, user, password, db_name, schema_name


# здесь пока берется время из datatime.now() Так что надо будет поменять!!


# метод запроса в целом. его можно юзать, когда надо сделть insert, update, delete
# в обшем когда не нужно ничего возвращать
def exec_query(update, info_message, query_type: bool):
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
            if query_type:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
        return result
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


# здесь возвращаются все результаты запроса для select
def exec_query_all(query, info_message):
    return exec_query(query, info_message, True)


# здесь возвращается первый результат запроса для select
def exec_query_first(query, info_message):
    return exec_query(query, info_message, False)


def add_user(name, password):
    exec_query(f"""insert into {schema_name}.users (name, password)
                          values ('{name}', '{password}')""",
               "[INFO] User was added", True)


def add_map(id_user, name, address):
    exec_query(f"""insert into {schema_name}.map (id_user, name, address)
                          values ({id_user}, '{name}', '{address}')""",
               "[INFO] Map was added", True)


def add_location(name, coord: list, id_map, floor):
    exec_query(f"""insert into {schema_name}.location (name, coord, id_map, floor)
                          values ('{name}', point({coord[0]}, {coord[1]}), {id_map}, {floor})""",
               "[INFO] Location was added", True)


def add_wall(id_location, coord_start: list, coord_end: list):
    exec_query(f"""insert into {schema_name}.wall (id_location, coord_start, coord_end)
                          values ({id_location}, point({coord_start[0]}, {coord_start[1]}),
                                                 point({coord_end[0]}, {coord_end[1]}))""",
               "[INFO] Wall was added", True)


def add_camera(id_location, coord: list, angle, width):
    exec_query(f"""insert into {schema_name}.camera (id_location, coord, angle, width)
                 values ({id_location}, point({coord[0]}, {coord[1]}), {angle}, {width})""",
               "[INFO] Camera was added", True)


def add_blind_line(coord_start: list, coord_end: list, id_camera1, id_camera2):
    exec_query(f"""insert into {schema_name}.blind_line (coord_start, coord_end, id_camera1, id_camera2)
                 values (point({coord_start[0]}, {coord_start[1]}), point({coord_end[0]}, {coord_end[1]}),
                        {id_camera1}, {id_camera2})""",
               "[INFO] Blind line was added", True)


def add_appearance(id_person, id_camera, data_time: datetime):
    exec_query(f"""insert into {schema_name}.appearance (id_person, id_camera, data_time)
                 values ({id_person}, {id_camera}, {ps.extensions.adapt(data_time)})""",
               "[INFO] Appearance was added", True)


def add_person(name, time_in, rime_out):
    exec_query(f"""insert into {schema_name}.person (name, time_in, time_out)
                 values ('{name}', {ps.extensions.adapt(time_in)}, {ps.extensions.adapt(rime_out)})""",
               "[INFO] Person was added", True)


def add_photo(vector: list, id_person):
    exec_query(f"""insert into {schema_name}.photo (vector, id_person)
                 values (Array[{vector}], {id_person})""",
               "[INFO] Photo was added", True)


def get_person_photo_vectors(id_person):
    return exec_query_first(f"""select p.vector
                                    from {schema_name}.photo p join {schema_name}.person p2 on p.id = p2.id_photo
                                    where p2.id = {id_person}""",
                            "[INFO] Person's photo-vectors was received")


def get_walls_in_location(id_location):
    return exec_query_first(f"""select w.coord_start, w.coord_end 
                                        from {schema_name}.wall w join {schema_name}.location l on w.id_location = l.id 
                                        where l.id = {id_location}""",
                            "[INFO] Location walls was received")


def get_locations_in_map(id_map):
    return exec_query_all(f"""select l.id, l."name", l.coord, l.floor
                                    from {schema_name}.location l join {schema_name}.map m on l.id_map = m.id 
                                    where m.id = {id_map}""",
                          "[INFO] Map locations was received")


def get_user_maps(id_map):
    return exec_query_all(f"""select m.id, m."name", m.address 
                                from {schema_name}.users u join {schema_name}."map" m on u.id = m.id_user 
                                where u.id = {id_map}""",
                          "[INFO] User maps was received")


def get_location_cameras(id_location):
    return exec_query_all(f"""select c.id, c.coord, c.angle, c.width 
                                from {schema_name}."location" l join {schema_name}.camera c on c.id_location = l.id 
                                where l.id = {id_location}""",
                          "[INFO] Location cameras were received")


def get_blind_line(id_camera):
    return exec_query_all(f"""select b.coord_start, b.coord_end 
                                    from {schema_name}.blind_line b
                                    where b.id_camera1  = {id_camera} or b.id_camera2  = {id_camera}""",
                          "[INFO] Blind line were received")


def get_person_appearances(id_person):
    return exec_query_first(f"""select a.id, a.id_camera, a.data_time 
                                       from {schema_name}.appearance a join {schema_name}.person p on a.id_person = p.id 
                                       where p.id = {id_person}""",
                            "[INFO] Person appearances were received")


def get_all_person():
    return exec_query_all(f"""select p.id from {schema_name}.person p""", '[INFO] Persons were received}')


if __name__ == "__main__":
    pass
    # add_photo(4, 3, 'photo5')