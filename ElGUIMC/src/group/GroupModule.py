from src.utils.singleton import Singleton
from src.group.GroupSet import GroupSet
from src.group.Group import Group
from src.group.GroupMapper import GroupMapper

MAX_GROUPS_NUMBER = 7
group_set = GroupSet()
group_mapper = GroupMapper()


class GroupModule(metaclass=Singleton):
    def __init__(self):
        pass

    # Проверка на основе сведений о предметной области (бизнес-логика)
    def check_and_create(self, name, description):
        group = group_set.find(name, description)
        if not group:
            group = Group(name, description)
            group_mapper.insert(group)
            group_set.add_group(group)

    def check_groups_number(self):
        group_mapper.load_all()
        groups_number = group_set.get_groups_number()
        if groups_number >= MAX_GROUPS_NUMBER:
            return False
        return True

    def get_groups_list(self):
        group_mapper.load_all()
        return group_set

    def get_single_group(self, group_id):
        group_mapper.load(group_id)
        group = group_set.find_by_id(group_id)
        return group
