from src.utils.singleton import Singleton
from src.criteria.CriteriaSet import CriteriaSet
from src.criteria.Criteria import Criteria
from src.criteria.CriteriaMapper import CriteriaMapper

criteria_set = CriteriaSet()
criteria_mapper = CriteriaMapper()


class CriteriaModule(metaclass=Singleton):
    def __init__(self):
        pass

    # Проверка на основе сведений о предметной области (бизнес-логика)
    def check_and_create(self, name, weight, measure, group_id):
        criteria = criteria_set.find(name, measure)
        if not criteria:
            criteria = Criteria(name, weight, measure, group_id)
            criteria_mapper.insert(criteria)
            criteria_set.add_criteria(criteria)
            return criteria.id

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
