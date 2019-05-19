from src.utils.singleton import Singleton


class ValueSet(metaclass=Singleton):
    def __init__(self):
        self.values = []

    def find_by_all_fields(self, value, assignment_time, criteria_id):
        return next((obj for obj in self.values if float(obj.value) == float(value) and
                     str(obj.assignment_time) == assignment_time.strftime("%Y-%m-%d %H:%M:%S") and
                     int(obj.criteria_id) == int(criteria_id)), None)

    def add_value(self, value_obj):
        self.values.append(value_obj)
