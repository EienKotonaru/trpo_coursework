from src.request.RequestStrategy import RequestStrategy
from src.request.RequestSet import RequestSet
from src.request.Request import Request

request_set = RequestSet()


class DocsRequestStrategy(RequestStrategy):
    def insert(self, request_obj):
        return "INSERT INTO docsrequests(status, student_id, quantity, purpose) VALUES ('{}', {}, {}, '{}') RETURNING id;" \
            .format(request_obj.status, request_obj.student_id, request_obj.quantity, request_obj.purpose)

    def delete(self, request_obj):
        return "DELETE FROM docsrequests WHERE id={};".format(request_obj.id)

    def load_all(self, cursor):
        cursor.execute("SELECT * FROM docsrequests;")
        request_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for request_entry in request_entries:
            request_obj = request_set.find_docs_by_all_fields(request_entry[cols_order.index("finish_time")],
                                                              request_entry[cols_order.index("status")],
                                                              request_entry[cols_order.index("student_id")],
                                                              quantity=request_entry[cols_order.index("quantity")],
                                                              purpose=request_entry[cols_order.index("purpose")],
                                                              creation_time=request_entry[cols_order.index("creation_time")])
            if not request_obj:
                request_obj = Request(request_entry[cols_order.index("finish_time")],
                                      request_entry[cols_order.index("status")],
                                      request_entry[cols_order.index("student_id")],
                                      quantity=request_entry[cols_order.index("quantity")],
                                      purpose=request_entry[cols_order.index("purpose")],
                                      creation_time=request_entry[cols_order.index("creation_time")],
                                      id=request_entry[cols_order.index("id")])
                request_set.add_request(request_obj)
