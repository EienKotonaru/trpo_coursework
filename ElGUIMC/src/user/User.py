class User:
    def __init__(self, email, password, role_id, profile_id, id=0):
        self.id = id
        self.email = email
        self.password = password
        self.profile_id = profile_id
        self.role_id = role_id

    def set_id(self, id):
        self.id = id