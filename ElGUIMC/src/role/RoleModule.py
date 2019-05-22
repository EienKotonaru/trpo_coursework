import binascii

from src.utils.singleton import Singleton
from src.role.RoleMapper import RoleMapper
from flask import redirect, request, url_for
from src.role.RoleSet import RoleSet


role_set = RoleSet()
role_mapper = RoleMapper()


class RoleModule(metaclass=Singleton):
    def __init__(self):
        pass

    def check_permission(self, id):
        role_mapper.load_all()
        role = role_set.find_by_id(id)
        url_name = request.url_rule.endpoint

        if url_name in role.pages:
            return True
        return False

    def get_role_id(self, role_name):
        if role_name:
            role_mapper.load_all()
            role = role_set.find_by_name(role_name)
            return role.id
        return None

        """criteria = user_set.find(email, password)
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
            criteria_set.remove_criteria(criteria_to_delete)"""
