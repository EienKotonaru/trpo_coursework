from src.utils.singleton import Singleton


class TsrSet(metaclass=Singleton):
    def __init__(self):
        self.tsrs = []

    def find_by_id(self, id):
        return next((obj for obj in self.tsrs if int(obj.id) == int(id)), None)

    def find_by_all_fields(self, manufacturer, usage_since_year, type, student_id):
        return next((obj for obj in self.tsrs if obj.manufacturer == manufacturer and
                     obj.usage_since_year == usage_since_year and
                     obj.type == type and
                     int(obj.student_id) == int(student_id)), None)

    def add_tsr(self, tsr_obj):
        self.tsrs.append(tsr_obj)

    def remove_tsr(self, tsr_obj):
        self.tsrs.remove(tsr_obj)