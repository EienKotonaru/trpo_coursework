class StudentCriteria:
    def __init__(self, student_id, criteria_id, weight, id=0):
        self.id = id
        self.student_id = student_id
        self.criteria_id = criteria_id
        self.weight = weight
        self.id = id

    def set_id(self, id):
        self.id = id