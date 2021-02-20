from abc import ABC, abstractmethod

class DBInterface(ABC):
    def __init__(self):
        pass
    #implementing creating user code
    @abstractmethod
    def create_user(self, name):
        raise NotImplementedError("create_user method not implemented!")
    #implementing change user code
    @abstractmethod
    def change_user(self, new_name, id):
        raise NotImplementedError("change_user method not implemented!")
    #implementing get user by id code
    @abstractmethod
    def get_user_by_id(self, id):
        raise NotImplementedError("get_user_by_id method not implemented!")
    #implementing delete user code
    @abstractmethod
    def delete_user(self, id):
        raise NotImplementedError("delete_user method not implemented!")
