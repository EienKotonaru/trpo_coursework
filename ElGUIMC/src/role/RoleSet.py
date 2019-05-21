from src.utils.singleton import Singleton


class RoleSet(metaclass=Singleton):
    def __init__(self):
        self.roles = []

    def find_by_id(self, id):
        return next((obj for obj in self.roles if int(obj.id) == int(id)), None)

    def find_by_all_fields(self, name, pages):
        return next((obj for obj in self.roles if obj.name == name
                     and obj.pages == pages), None)

    def add_role(self, role_obj):
        self.roles.append(role_obj)

    def remove_role(self, role_obj):
        self.roles.remove(role_obj)
