from src.utils.singleton import Singleton
from src.request.RequestSet import RequestSet
from src.request.Request import Request
from src.request.RequestDocsStrategy import DocsRequestStrategy
from src.request.RequestTsrsStrategy import TsrsRequestStrategy
from src.request.RequestMapper import RequestMapper

request_set = RequestSet()
request_mapper = RequestMapper(DocsRequestStrategy)


class RequestModule(metaclass=Singleton):
    def __init__(self):
        pass

    def create_request(self, finish_time, status, student_id, quantity=None, purpose=None, problem=None, tsr_id=None):
        request = Request(finish_time, status, student_id, quantity, purpose, problem, tsr_id)
        if quantity and purpose:
            request_mapper.strategy = DocsRequestStrategy()
        if problem and tsr_id:
            request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.insert(request)
        request_set.add_request(request)

    def get_student_requests(self, student_id):
        request_mapper.strategy = DocsRequestStrategy()
        request_mapper.load_all()

        request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.load_all()

        result = request_set

        return list(filter(lambda obj: int(obj.student_id) == int(student_id), result.requests))

    def remove_request(self, request_id):
        request_mapper.strategy = DocsRequestStrategy()
        request_mapper.load_all()

        request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.load_all()
        request = request_set.find_by_id(request_id)
        if request.quantity and request.purpose:
            request_mapper.strategy = DocsRequestStrategy()
        if request.problem and request.tsr_id:
            request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.delete(request)
        request_set.remove_request(request)

    def create_tsr(self, manufacturer, usage_since_year, type, student_id):
        tsr_mapper.load_all()
        tsr = Tsr(manufacturer, usage_since_year, type, student_id)
        tsr_mapper.insert(tsr)
        tsr_set.add_tsr(tsr)

    def update_tsr(self, manufacturer, usage_since_year, type, id):
        tsr_mapper.load_all()
        tsr = tsr_set.find_by_id(id)
        tsr.manufacturer, tsr.usage_since_year, tsr.type = manufacturer, usage_since_year, type
        tsr_mapper.update(tsr)

    def get_tsrs_list(self):
        tsr_mapper.load_all()
        return tsr_set.tsrs

    def get_tsrs_by_student(self, student_id):
        tsr_mapper.load_all()
        tsrs_by_student = tsr_set.tsrs
        tsrs_by_student = [obj for obj in tsrs_by_student if int(obj.student_id) == int(student_id)]
        return tsrs_by_student

    def remove_tsr(self, tsr_id):
        tsr_mapper.load_all()
        tsr_to_delete = tsr_set.find_by_id(tsr_id)
        if tsr_to_delete:
            tsr_mapper.delete(tsr_to_delete)
            tsr_set.remove_tsr(tsr_to_delete)
