from abc import ABC, abstractmethod


class RequestStrategy(ABC):
    @abstractmethod
    def insert(self, request_obj):
        pass

    @abstractmethod
    def delete(self, request_obj):
        pass

    @abstractmethod
    def update(self, request_obj):
        pass

    @abstractmethod
    def load_all(self, cursor):
        pass