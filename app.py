from response_utils import ResponseUtils as r
from flask import Flask, request
#читаем файл с конфигами
cfg = open("config", "r").read().split('\n')
cfg_values = {}
#парсим значения в словарь
for param in cfg:
    name, value = param.split('=')
    cfg_values[name] = value
#инициализируем в соответствии с б.д.
if cfg_values['REPOSITORY_TYPE'] == 'sqlite':
    from db_scrpits.sqlite.sqlite_db import SqliteDB
    db = SqliteDB()
    if cfg_values['IF_SQLITE_RECREATE_DB'] == 'yes':
        db.recreate_db()

elif cfg_values['REPOSITORY_TYPE'] == 'postgres':
    from db_scrpits.postgres_db import PostgreDB
    db = PostgreDB(dbname=cfg_values['POSTGRE_SQL_DB_NAME'], user=cfg_values['POSTGRE_SQL_USER'],
                   password=cfg_values['POSTGRE_SQL_PASSWORD'], host=cfg_values['POSTGRE_SQL_HOST'])

elif cfg_values['REPOSITORY_TYPE'] == 'memory':
    from db_scrpits.memory_db import MemoryDB
    db = MemoryDB()
#стартуем сервер
app = Flask(__name__)

#опишу для одного обработчика запроса
#запрос на создание юзера
@app.route('/create_user', methods=['POST'])
def create_user():
    #забираем имя из квери параметров
    name = request.args.get('name')
    #проверяем передели ли нам такой параметр
    if name == None:
        #если не передали возвращаем ошибку и код 400, см. response_utils
        return r.miss_parameter('name')
    #делаем запрос в б.д.
    return db.create_user(name)


@app.route('/get_user_by_id', methods=['GET'])
def get_user_by_id():
    id = request.args.get('id')
    if id == None:
        return r.miss_parameter('id')

    return db.get_user_by_id(id)


@app.route('/change_user', methods=['POST'])
def change_user():
    id = request.args.get('id')
    if id == None:
        return r.miss_parameter('id')
    new_name = request.args.get('new_name')
    if new_name == None:
        return r.miss_parameter('name')

    return db.change_user(new_name, id)


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    id = request.args.get('id')
    if id == None:
        return r.miss_parameter('id')

    return db.delete_user(id)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return r.miss_page()
