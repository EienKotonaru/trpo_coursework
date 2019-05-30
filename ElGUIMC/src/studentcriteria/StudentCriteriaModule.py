from src.utils.singleton import Singleton
from src.studentcriteria.StudentCriteria import StudentCriteria
from src.studentcriteria.StudentCriteriaSet import StudentCriteriaSet
from src.studentcriteria.StudentCriteriaMapper import StudentCriteriaMapper

student_criteria_set = StudentCriteriaSet()
student_criteria_mapper = StudentCriteriaMapper()


class StudentCriteriaModule(metaclass=Singleton):
    def __init__(self):
        pass

    def assign_criterias(self, criterias, student_id):
        student_criteria_mapper.load_all()
        for (criteria, weight) in criterias.items():
            if weight:
                student_criteria = student_criteria_set.find_by_ids(student_id, criteria)
                if not student_criteria:
                    student_criteria = StudentCriteria(student_id, criteria, weight)
                    student_criteria_mapper.insert(student_criteria)
                    student_criteria_set.add_student_criteria(student_criteria)
                else:
                    student_criteria.weight = weight
                    student_criteria_mapper.update(student_criteria)

    def get_student_criterias_list(self, student_id):
        student_criteria_mapper.load_all()
        result = list(filter(lambda obj: int(obj.student_id) == int(student_id), student_criteria_set.student_criterias))
        return result
