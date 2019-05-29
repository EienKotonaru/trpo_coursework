class Request:
    def __init__(self, finish_time, status, student_id, quantity=None, purpose=None, problem=None, tsr_id=None,
                 creation_time=None, id=0):
        self.id = id
        self.creation_time = creation_time
        self.finish_time = finish_time
        self.status = status
        self.student_id = student_id
        self.quantity = quantity
        self.purpose = purpose
        self.problem = problem
        self.tsr_id = tsr_id

    def set_id(self, id):
        self.id = id