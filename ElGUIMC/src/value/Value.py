class Value:
    def __init__(self, value, assignment_time, criteria_id, id=0):
        self.id = id
        self.value = value
        self.assignment_time = assignment_time
        self.criteria_id = criteria_id

    def set_id(self, id):
        self.id = id