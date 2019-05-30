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
        request_mapper.strategy = DocsRequestStrategy()
        request_mapper.load_all()

        request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.load_all()

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

    def get_request_by_id(self, request_id):
        request_mapper.strategy = DocsRequestStrategy()
        request_mapper.load_all()

        request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.load_all()
        request = request_set.find_by_id(request_id)
        if request.quantity and request.purpose:
            request_mapper.strategy = DocsRequestStrategy()
        if request.problem and request.tsr_id:
            request_mapper.strategy = TsrsRequestStrategy()
        return next((obj for obj in request_set.requests if int(obj.id) == int(request_id)), None)
