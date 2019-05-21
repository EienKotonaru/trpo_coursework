from src.utils.singleton import Singleton


class ProfileSet(metaclass=Singleton):
    def __init__(self):
        self.profiles = []

    def find_by_uuid(self, uuid):
        return next((obj for obj in self.profiles if obj.uuid == uuid), None)

    def find_by_id(self, id):
        return next((obj for obj in self.profiles if int(obj.id) == int(id)), None)

    def add_profile(self, profile_obj):
        self.profiles.append(profile_obj)

    def remove_profile(self, profile_obj):
        self.profiles.remove(profile_obj)
