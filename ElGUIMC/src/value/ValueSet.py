from src.utils.singleton import Singleton


class ValueSet(metaclass=Singleton):
    def __init__(self):
        self.values = []

    def find_by_all_fields(self, value, assignment_time, criteria_id, student_id):
        return next((obj for obj in self.values if float(obj.value) == float(value) and
                     obj.assignment_time == assignment_time and
                     int(obj.criteria_id) == int(criteria_id) and
                     int(obj.student_id) == int(student_id)), None)

    def find_by_student(self, student_id):
        return list(filter(lambda obj: int(obj.student_id) == int(student_id), self.values))

    def add_value(self, value_obj):
        self.values.append(value_obj)
