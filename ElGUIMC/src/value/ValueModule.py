from src.utils.singleton import Singleton
from src.value.ValueSet import ValueSet
from src.value.Value import Value
from src.value.ValueMapper import ValueMapper
from time import localtime

value_set = ValueSet()
value_mapper = ValueMapper()


class ValueModule(metaclass=Singleton):
    def __init__(self):
        pass

    def get_values_history(self, criterias, student_id):
        value_mapper.load_all()
        values_by_criterias = value_set.values
        result = {}
        for criteria in criterias:
            filtered_values = [obj for obj in values_by_criterias if int(obj.criteria_id) == int(criteria.id) and int(obj.student_id) == int(student_id)]
            result[criteria] = filtered_values
        return result

    def get_values_by_student(self, student_id):
        value_mapper.load_all()
        result = value_set.find_by_student(student_id)
        return result

    def create_values_for_criterias(self, value_list, criteria_id_list, student_id):
        value_criteria_list = list(zip(value_list, criteria_id_list))
        current_time = localtime()
        for value_criteria in value_criteria_list:
            value_obj = Value(float(value_criteria[0]), current_time, value_criteria[1], student_id)
            value_mapper.insert(value_obj)

    def prepare_statistics(self, student_id, criterias):
        values = self.get_values_by_student(student_id)
        statistics = {}
        for value in values:
            if value.assignment_time not in statistics.keys():
                statistics[value.assignment_time.strftime('%Y-%m-%d %H:%M:%S')] = 0
        for date in statistics.keys():
            for value in values:
                if date == value.assignment_time.strftime('%Y-%m-%d %H:%M:%S'):
                    weight = list(filter(lambda crit: int(crit.criteria_id) == int(value.criteria_id) and int(crit.student_id) == int(value.student_id), criterias))[0].weight
                    statistics[value.assignment_time.strftime('%Y-%m-%d %H:%M:%S')] += value.value * weight
        return statistics
