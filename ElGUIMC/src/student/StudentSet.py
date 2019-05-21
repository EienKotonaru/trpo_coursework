from src.utils.singleton import Singleton


class StudentSet(metaclass=Singleton):
    def __init__(self):
        self.students = []

    def find_by_uuid(self, uuid):
        return next((obj for obj in self.students if obj.uuid == uuid), None)

    def find_by_id(self, id):
        return next((obj for obj in self.students if int(obj.id) == int(id)), None)

    def add_student(self, student_obj):
        self.students.append(student_obj)

    def remove_student(self, student_obj):
        self.students.remove(student_obj)
