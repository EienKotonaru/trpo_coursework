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

    def get_single_role(self, role_id):
        role_mapper.load_all()
        return role_set.find_by_id(role_id)

    def get_roles_list(self):
        role_mapper.load_all()
        return role_set.roles

    def update_pages(self, role_id, page, index):
        role = self.get_single_role(role_id)
        role.pages[int(index)] = page
        role_mapper.update(role)
        return

    def delete_page(self, role_id, index):
        role = self.get_single_role(role_id)
        del role.pages[int(index)]
        role_mapper.update(role)
        return

    def add_page(self, role_id, page):
        role = self.get_single_role(role_id)
        role.pages.append(page)
        role_mapper.update(role)
        return
