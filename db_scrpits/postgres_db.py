import psycopg2
from db_scrpits.db_interface import DBInterface
from response_utils import ResponseUtils as r


class PostgreDB(DBInterface):
    #сохраняем параметры подключения
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
    #получает подключение к б.д.
    def get_connection(self):
        #пробуем подключиться
        try:
            conn = psycopg2.connect(dbname=self.dbname, user=self.user,
                                    password=self.password, host=self.host)
            #чтобы сохранять изменения
            conn.autocommit = True
            return conn
        #если подключиться не вышло
        except psycopg2.Error as e:
            print("Error while connecting to postgres", e)
            return None
    #выполняет запросы к б.д.
    def execute(self, to_execute, arguments, with_row_count=False, with_return=False):
        #получили подключение
        conn = self.get_connection()
        #проверили что оно есть
        if conn == None:
            print("Error while connecting to postgres")
            #далее такая запись означает, что запрос был сделан
            #из функции, которая хочет назад 2 аргумента
            if with_row_count:
                return None, None
            return None
        #получаем курсор
        cur = conn.cursor()
        #пробуем выполнить запрос
        try:
            cur.execute(to_execute, arguments)
            #следующий финт связан с тем, что после execute,
            #если запрос ничего не возвращает, нельзя делать fetchall()
            #поэтому заранее узнаем через with_return будет ли у запроса ответ
            result = 'OK'
            if with_return:
                result = cur.fetchall()
            #узнаём сколько строк изменили
            row_count = cur.rowcount
        #если запрос не был выполнен корректно
        except psycopg2.Error as e:

            print("Error while execute", e)
            if with_row_count:
                return None, None
            return None
        #закрываем соединение с б.д.
        conn.close()
        #если нужно число измененных строк возвращаем с row_count
        if with_row_count:
            return result, row_count
        else:
            return result
    #функция запроса к б.д.
    def create_user(self, name):
        #делаем запрос
        result = self.execute("""
                INSERT
                INTO users 
                (fullname) VALUES (%s)
                """, (name,))
        #в зависимости от того что вернул запрос
        #или как подключились к б.д.
        #делаем ответ клиенту см. в response_utils
        if result != None:
            return r.return_ok()
        else:
            return r.internal_error('failed to create user')
    #функция изменения имени
    def change_user(self, new_name, id):
        #запрос
        result, rows = self.execute("""
                UPDATE users 
                SET fullname=%s 
                WHERE id=%s
                """, (new_name, id), with_row_count=True)
        #проверяем на ошибку
        if result == None:
            return r.internal_error('failed while change user name')
        #если запрос вернул 0 как число измененных строк
        #значит такого id не оказалось
        if rows == 0:
            return r.wrong_parameters('user doesnt exist')
        return r.return_ok()
    #функция получения юзера по ид
    def get_user_by_id(self, id):
        #запрос
        result = self.execute("""
                SELECT fullname 
                FROM users 
                WHERE id=%s
                """, (id,), with_return=True)
        #запрос может вернуть пустой список значит id не суеществует
        if not result:
            return r.wrong_parameters('user doesnt exist')
        #проверяем на корректность запроса
        if result != None:
            #Ну т.к. структура ответа с б.д. list[fields_value[]],
            #а наш запрос может получить только одного пользователя
            #То ответ будет вида [[fullname]]
            user = result[0][0]
            return r.return_ok(user)
        else:
            return r.internal_error('failed while get user')
    #функция удаления юзера
    def delete_user(self, id):
        #запрос
        result, rows = self.execute("""
                DELETE 
                FROM users 
                WHERE id=%s
                """, (id,), with_row_count=True)
        #проверяем что всё прошло хорошо
        if result == None:
            return r.internal_error('failed while delete user')
        #проверяем что пользователь существовал, по аналогии change_user()
        if rows == 0:
            return r.wrong_parameters('user doesnt exist')
        return r.return_ok()
