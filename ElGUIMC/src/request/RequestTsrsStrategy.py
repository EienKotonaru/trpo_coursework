from src.request.RequestStrategy import RequestStrategy
from src.request.RequestSet import RequestSet
from src.request.Request import Request

request_set = RequestSet()


class TsrsRequestStrategy(RequestStrategy):
    def insert(self, request_obj):
        return "INSERT INTO tsrsrequests(status, student_id, problem, tsr_id) VALUES ('{}', {}, '{}', {}) RETURNING id, creation_time;" \
            .format(request_obj.status, request_obj.student_id, request_obj.problem, request_obj.tsr_id)

    def delete(self, request_obj):
        return "DELETE FROM tsrsrequests WHERE id={};".format(request_obj.id)

    def update(self, request_obj):
        return "UPDATE tsrsrequests SET status='{}', student_id={}, problem='{}', tsr_id={} WHERE id={};"\
            .format(request_obj.status, request_obj.student_id, request_obj.problem, request_obj.tsr_id, request_obj.id)

    def load_all(self, cursor):
        cursor.execute("SELECT * FROM tsrsrequests;")
        request_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for request_entry in request_entries:
            request_obj = request_set.find_tsrs_by_all_fields(request_entry[cols_order.index("finish_time")],
                                                              request_entry[cols_order.index("status")],
                                                              request_entry[cols_order.index("student_id")],
                                                              problem=request_entry[cols_order.index("problem")],
                                                              tsr_id=request_entry[cols_order.index("tsr_id")],
                                                              creation_time=request_entry[cols_order.index("creation_time")])
            if not request_obj:
                request_obj = Request(request_entry[cols_order.index("finish_time")],
                                      request_entry[cols_order.index("status")],
                                      request_entry[cols_order.index("student_id")],
                                      problem=request_entry[cols_order.index("problem")],
                                      tsr_id=request_entry[cols_order.index("tsr_id")],
                                      creation_time=request_entry[cols_order.index("creation_time")],
                                      id=request_entry[cols_order.index("id")])
                request_set.add_request(request_obj)
