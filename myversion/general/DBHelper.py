import psycopg2
import inspect


class DBHelper:
    def __init__(self, database, user, password, host):
        self.__con = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.__cur = self.__con.cursor()

    def exec(self, command, array=None):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        if array is not None:
            self.__cur.execute(command, (array, ))
        else:
            self.__cur.execute(command)
        self.__con.commit()

    def record_exist(self, id_, table):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        self.exec(f'select * from {table} where id = {id_}')
        return self.fetch_all()

    def fetch_one(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        return self.__cur.fetchone()

    def fetch_many(self, n):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        return self.__cur.fetchmany(n)

    def fetch_all(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print('caller name:', calframe[1][3])
        return self.__cur.fetchall()

    def __del__(self):
        self.__cur.close()
        self.__con.close()

