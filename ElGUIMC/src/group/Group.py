class Group:
    def __init__(self, name, description, id=0):
        self.id = id
        self.name = name
        self.description = description

    def set_id(self, id):
        self.id = id