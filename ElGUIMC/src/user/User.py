class User:
    def __init__(self, email, password, uuid, role_id, id=0):
        self.id = id
        self.email = email
        self.password = password
        self.uuid = uuid
        self.role_id = role_id

    def set_id(self, id):
        self.id = id