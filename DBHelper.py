import psycopg2


class DBHelper:
    def __init__(self, database, user, password, host):
        self.__con = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.__cur = self.__con.cursor()

    def exec(self, command, array=None):
        if array:
            self.__cur.execute(command, (array, ))
        else:
            self.__cur.execute(command)
        self.__con.commit()

    def record_exist(self, id_, table):
        self.exec(f'select * from {table} where id = {id_}')
        return self.fetch_all()

    def fetch_one(self):
        return self.__cur.fetchone()

    def fetch_many(self, n):
        return self.__cur.fetchmany(n)

    def fetch_all(self):
        return self.__cur.fetchall()

    def __del__(self):
        self.__cur.close()
        self.__con.close()

