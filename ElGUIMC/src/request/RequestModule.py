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

    def create_request(self, finish_time, status, student_id, quantity=0, purpose=None, problem=None, tsr_id=0):
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

        filtered = list(filter(lambda obj: int(obj.student_id) == int(student_id), result.requests))

        return sorted(filtered, key=lambda obj: int(obj.id), reverse=True)

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

        return next((obj for obj in request_set.requests if int(obj.id) == int(request_id)), None)

    def get_all_requests(self):
        request_mapper.strategy = DocsRequestStrategy()
        request_mapper.load_all()

        request_mapper.strategy = TsrsRequestStrategy()
        request_mapper.load_all()

        return sorted(request_set.requests, key=lambda obj: int(obj.id), reverse=True)

    def change_request_status(self, request_id, new_status):
        request = self.get_request_by_id(request_id)
        request.status = new_status
        request_mapper.update(request)