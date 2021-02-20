from db_scrpits.db_interface import DBInterface
from response_utils import ResponseUtils as r

#реализация в памяти
class MemoryDB(DBInterface):
    #инициализируем стартовый id и словарь пользователей
    def __init__(self, dbname='users'):
        self.next_id = 1
        self.users = {}
    #создаёт юзера
    def create_user(self, name):
        #получаем id для пользователя
        id = self.get_new_id()
        #создаём значение в словаре
        self.users[str(id)] = name
        #возвращаем хороший ответ
        return r.return_ok()
    #меняет юзера
    def change_user(self, new_name, id):
        #далее везде нужен каст к int, т.к. первоначально
        #id - строковые
        #проверяем есть ли пользователь
        if self.users.get(int(id)) == None:
            return r.wrong_parameters('nothing to change, user doesnt exist')
        else:
            #присваиваем новое имя
            self.users[int(id)] = new_name
        return r.return_ok()
    #возвращает юзера
    def get_user_by_id(self, id):
        user = self.users.get(int(id))
        #проверяем существует ли юзер
        if user != None:
            return r.return_ok(user)
        else:
            #юзера не существует
            return r.wrong_parameters('user doesnt exist')
    #удаляет юзера
    def delete_user(self, id):
        #пробуем удалить
        try:
            self.users.pop(int(id))
            return r.return_ok()
        #пользователя не сущестовало
        except:
            return r.wrong_parameters('user doesnt exist')
    #получаем новые id
    #просто будем прибавлять единичку,
    #никогда не повторимся
    def get_new_id(self):
        id = self.next_id
        self.next_id += 1
        return id
