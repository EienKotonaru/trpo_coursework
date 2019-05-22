class Profile:
    def __init__(self, last_name, first_name, birth_date, gender, uuid, phone=None, middle_name=None, relname=None, id=0):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.uuid = uuid
        self.phone = phone
        self.middle_name = middle_name
        self.relname = relname

    def set_id(self, id):
        self.id = id