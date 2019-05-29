from src.profile.Profile import Profile


class Employee(Profile):
    def __init__(self, last_name, first_name, birth_date, gender, uuid,
                 middle_name=None, phone=None, work_auditory=None, title=None, degree=None, id=0):
        super().__init__(last_name, first_name, birth_date, gender, uuid, phone, middle_name, id)
        self.work_auditory = work_auditory
        self.title = title
        self.degree = degree

    def set_id(self, id):
        self.id = id