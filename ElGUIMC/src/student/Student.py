from src.profile.Profile import Profile


class Student(Profile):
    def __init__(self, last_name, first_name, birth_date, gender, uuid,
                 speciality, citizenship, group, enrollment, studying_type, grade_card,
                 phone=None, middle_name=None, dormitory=False, address=None, id=0):
        super().__init__(last_name, first_name, birth_date, gender, uuid, phone, middle_name, id)
        self.speciality = speciality
        self.citizenship = citizenship
        self.group = group
        self.enrollment = enrollment
        self.studying_type = studying_type
        self.grade_card = grade_card
        self.dormitory = dormitory
        self.address = address

    def set_id(self, id):
        self.id = id