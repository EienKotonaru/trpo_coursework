from src.utils.singleton import Singleton


class CriteriaSet(metaclass=Singleton):
    def __init__(self):
        self.criterias = []

    def find(self, name):
        return next((obj for obj in self.criterias if obj.name == name), None)

    def find_by_all_fields(self, name, measure, group_id):
        return next((obj for obj in self.criterias if obj.name == name and
                     obj.measure == measure and
                     int(obj.group_id) == int(group_id)), None)

    def find_by_id(self, id):
        return next((obj for obj in self.criterias if int(obj.id) == int(id)), None)

    def add_criteria(self, criteria_obj):
        self.criterias.append(criteria_obj)

    def remove_criteria(self, criteria_obj):
        self.criterias.remove(criteria_obj)