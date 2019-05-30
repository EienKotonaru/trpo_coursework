from src.utils.singleton import Singleton


class RequestSet(metaclass=Singleton):
    def __init__(self):
        self.requests = []

    def find_by_id(self, id):
        return next((obj for obj in self.requests if int(obj.id) == int(id)), None)

    def find_docs_by_all_fields(self, finish_time, status, student_id, quantity=0, purpose=None, creation_time=None):
        return next((obj for obj in self.requests if obj.finish_time == finish_time and
                     obj.status == status and
                     int(obj.student_id) == int(student_id) and
                     int(obj.quantity) == int(quantity) and
                     obj.purpose == purpose and
                     obj.creation_time == creation_time), None)

    def find_tsrs_by_all_fields(self, finish_time, status, student_id, problem=None, tsr_id=0, creation_time=None):
        return next((obj for obj in self.requests if obj.finish_time == finish_time and
                     obj.status == status and
                     int(obj.student_id) == int(student_id) and
                     obj.problem == problem and
                     int(obj.tsr_id) == int(tsr_id) and
                     obj.creation_time == creation_time), None)

    def add_request(self, request_obj):
        self.requests.append(request_obj)

    def remove_request(self, request_obj):
        self.requests.remove(request_obj)
