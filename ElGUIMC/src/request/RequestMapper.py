from src.utils.singleton import Singleton
from src.request.RequestSet import RequestSet
from src.request.RequestStrategy import RequestStrategy
import psycopg2

request_set = RequestSet()


class RequestMapper(metaclass=Singleton):
    def __init__(self, strategy: RequestStrategy):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )
        self._strategy = strategy

    @property
    def strategy(self) -> RequestStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: RequestStrategy):
        self._strategy = strategy

    def insert(self, request_obj):
        cursor = self.db.cursor()
        sql_string = self._strategy.insert(request_obj)
        cursor.execute(sql_string)
        self.db.commit()
        result = cursor.fetchone()
        request_obj.set_id(result[0])
        request_obj.creation_time = result[1]
        cursor.close()

    def delete(self, request_obj):
        cursor = self.db.cursor()
        sql_string = self._strategy.delete(request_obj)
        cursor.execute(sql_string)
        self.db.commit()
        cursor.close()

    def load_all(self):
        cursor = self.db.cursor()
        self._strategy.load_all(cursor)
        cursor.close()

    def update(self, request_obj):
        cursor = self.db.cursor()
        sql_string = self._strategy.update(request_obj)
        cursor.execute(sql_string)
        self.db.commit()
        cursor.close()
