from src.utils.singleton import Singleton


class EmployeeSet(metaclass=Singleton):
    def __init__(self):
        self.employees = []

    def find_by_uuid(self, uuid):
        return next((obj for obj in self.employees if obj.uuid == uuid), None)

    def find_by_id(self, id):
        return next((obj for obj in self.employees if int(obj.id) == int(id)), None)

    def add_employee(self, employee_obj):
        self.employees.append(employee_obj)

    def remove_employee(self, employee_obj):
        self.employees.remove(employee_obj)
