
class ResponseUtils():
    #если есть возвращаемое значение, возвращаем его, если нет просто 'OK'
    @staticmethod
    def return_ok(response='OK'):
        return response, 200
    #если клиент не положил нужный параметр
    @staticmethod
    def miss_parameter(param_name):
        return 'Error: miss ' + param_name, 400
    #если сам параметр верный, но его значение
    #но при выполнении запроса значение не позволило что-то сделать
    @staticmethod
    def wrong_parameters(massage):
        return 'Error: ' + massage, 400
    #если клиент обратился на неверную ссылку
    @staticmethod
    def miss_page(massage='fake url'):
        return 'Error: ' + massage, 404
    #для внутренних ошибок
    @staticmethod
    def internal_error(error_massage):
        return 'Error: ' + error_massage, 500
