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

    def get_values_history(self, criterias):
        value_mapper.load_all()
        values_by_criterias = value_set.values
        result = {}
        for criteria in criterias:
            filtered_values = [obj for obj in values_by_criterias if int(obj.criteria_id) == int(criteria.id)]
            result[criteria] = filtered_values
        return result

    def create_values_for_criterias(self, value_list, criteria_id_list):
        value_criteria_list = list(zip(value_list, criteria_id_list))
        current_time = localtime()
        for value_criteria in value_criteria_list:
            value_obj = Value(float(value_criteria[0]), current_time, value_criteria[1])
            value_mapper.insert(value_obj)
