class Tsr:
    def __init__(self, manufacturer, usage_since_year, type, student_id, id=0):
        self.id = id
        self.manufacturer = manufacturer
        self.usage_since_year = usage_since_year
        self.type = type
        self.student_id = student_id

    def set_id(self, id):
        self.id = id