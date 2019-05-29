class Criteria:
    def __init__(self, name, measure, group_id, id=0):
        self.id = id
        self.name = name
        self.measure = measure
        self.group_id = group_id

    def set_id(self, id):
        self.id = id