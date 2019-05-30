from src.utils.singleton import Singleton
from src.criteria.CriteriaSet import CriteriaSet
from src.criteria.Criteria import Criteria
from src.criteria.CriteriaMapper import CriteriaMapper

criteria_set = CriteriaSet()
criteria_mapper = CriteriaMapper()


class CriteriaModule(metaclass=Singleton):
    def __init__(self):
        pass

    def check_and_create(self, name, measure, group_id):
        criteria_mapper.load_all()
        criteria = criteria_set.find(name)
        if not criteria:
            criteria = Criteria(name, measure, group_id)
            criteria_mapper.insert(criteria)
            criteria_set.add_criteria(criteria)
            return criteria.id
        else:
            criteria.measure = measure
            criteria_mapper.update(criteria)

    def get_criteria_by_id(self, criteria_id):
        criteria_mapper.load_all()
        return criteria_set.find_by_id(criteria_id)

    def get_criterias_list(self):
        criteria_mapper.load_all()
        return criteria_set.criterias

    def get_criterias_by_group(self, group_id):
        criteria_mapper.load_all()
        criterias_by_group = criteria_set.criterias
        criterias_by_group = [obj for obj in criterias_by_group if int(obj.group_id) == int(group_id)]
        return criterias_by_group

    def remove_criteria(self, criteria_id):
        criteria_mapper.load_all()
        criteria_to_delete = criteria_set.find_by_id(criteria_id)
        if criteria_to_delete:
            criteria_mapper.delete(criteria_to_delete)
            criteria_set.remove_criteria(criteria_to_delete)
