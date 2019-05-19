from src.utils.singleton import Singleton


class GroupSet(metaclass=Singleton):
    def __init__(self):
        self.groups = []

    def find(self, name, description):
        return next((obj for obj in self.groups if obj.name == name and obj.description == description), None)

    def find_by_id(self, id):
        return next((obj for obj in self.groups if obj.id == int(id)), None)

    def add_group(self, group_obj):
        self.groups.append(group_obj)

    def get_groups_number(self):
        return len(self.groups)
