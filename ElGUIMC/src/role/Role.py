class Role:
    def __init__(self, name, pages, id=0):
        self.id = id
        self.name = name
        self.pages = pages

    def set_id(self, id):
        self.id = id