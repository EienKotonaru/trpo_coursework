from src.utils.singleton import Singleton


class UserSet(metaclass=Singleton):
    def __init__(self):
        self.users = []

    def find_by_email_password(self, email, password):
        return next((obj for obj in self.users if obj.email == email
                     and obj.password == password), None)

    def find_by_profile(self, profile_id):
        return next((obj for obj in self.users if obj.profile_id == profile_id), None)

    def find_by_all_fields(self, email, password, profile_id, role_id):
        return next((obj for obj in self.users if obj.email == email
                     and obj.password == password
                     and obj.profile_id == profile_id
                     and obj.role_id == role_id), None)

    def find_by_id(self, id):
        return next((obj for obj in self.users if int(obj.id) == int(id)), None)

    def add_user(self, user_obj):
        self.users.append(user_obj)

    def remove_user(self, user_obj):
        self.users.remove(user_obj)