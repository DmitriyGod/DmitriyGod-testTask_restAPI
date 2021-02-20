from db_scrpits.db_interface import DBInterface
from response_utils import ResponseUtils as r
import sqlite3


class SqliteDB(DBInterface):
    #узнаём с какой б.д. будем работать
    def __init__(self, dbname='users'):
        self.dbname = dbname
    #если вдруг б.д. надо пересоздать или создать
    def recreate_db(self):
        connection = sqlite3.connect(self.dbname + '.db')
        #загрузили запрос из schema и исполнили на б.д. получили таблицу
        with open('schema.sql') as f:
            connection.executescript(f.read())
        connection.commit()
        connection.close()
    #получаем подключение
    def get_connection(self):
        #пробуем подключиться к б.д.
        try:
            connection = sqlite3.connect(self.dbname + '.db')
            #выбираем формат возвращаемых значений
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            print("Error while connecting to sqlite", e)
            return None
    #исполняет запрос, всё по аналогии с postgres (если что сначала посмотрите в постгрес)
    #за исключением того, что можно делать fetchall() и всё из этого вытекающее
    def execute(self, to_execute, arguments, with_row_count=False):
        conn = self.get_connection()
        if conn == None:
            print("Error while connecting to sqlite")
            if with_row_count:
                return None, None
            return None
        cur = conn.cursor()
        try:
            cur.execute(to_execute, arguments)
            result = cur.fetchall()
            row_count = cur.rowcount
            conn.commit()
        except sqlite3.Error as e:
            print("Error while execute", e)
            if with_row_count:
                return None, None
            return None

        conn.close()
        if with_row_count:
            return result, row_count
        else:
            return result
    #всё аналогично с postgres только немного по-другому формируем запросы
    def create_user(self, name):
        sql = """
                INSERT
                INTO users 
                (fullname) VALUES (?)
                """

        result = self.execute(sql, (name,))

        if result != None:
            return r.return_ok()
        else:
            return r.internal_error('failed to create user')

    def change_user(self, new_name, id):
        sql = """
                UPDATE users 
                SET fullname=? 
                WHERE person_id=?
                """
        result, rows = self.execute(sql, (new_name, id), with_row_count=True)

        if result == None:
            return r.internal_error('failed while change user name')
        if rows == 0:
            return r.wrong_parameters('user doesnt exist')
        return r.return_ok()

    def get_user_by_id(self, id):
        sql = """
                SELECT fullname 
                FROM users 
                WHERE person_id=?
                """
        result = self.execute(sql, (id,))

        if not result:
            return r.wrong_parameters('user doesnt exist')

        if result != None:
            user = result[0][0]
            return r.return_ok(user)
        else:
            return r.internal_error('failed while get user')

    def delete_user(self, id):
        sql = """
                DELETE 
                FROM users 
                WHERE person_id=?
                """
        result, rows = self.execute(sql, (id,), with_row_count=True)
        if result == None:
            return r.internal_error('failed while delete user')
        if rows == 0:
            return r.wrong_parameters('user doesnt exist')
        return r.return_ok()
