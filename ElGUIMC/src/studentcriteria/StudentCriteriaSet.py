from src.utils.singleton import Singleton


class StudentCriteriaSet(metaclass=Singleton):
    def __init__(self):
        self.student_criterias = []

    def find(self, student_id, criteria_id, weight):
        return next((obj for obj in self.student_criterias if int(obj.student_id) == int(student_id) and
                     int(obj.criteria_id) == int(criteria_id) and
                     int(obj.weight) == int(weight)), None)

    def find_by_ids(self, student_id, criteria_id):
        return next((obj for obj in self.student_criterias if int(obj.student_id) == int(student_id) and
                     int(obj.criteria_id) == int(criteria_id)), None)

    def find_by_id(self, id):
        return next((obj for obj in self.student_criterias if obj.id == int(id)), None)

    def add_student_criteria(self, sc_obj):
        self.student_criterias.append(sc_obj)

    def remove_student_criteria(self, sc_obj):
        self.student_criterias.remove(sc_obj)
