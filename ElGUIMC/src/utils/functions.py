from src.role.RoleModule import RoleModule
from src.user.UserModule import UserModule

role_module = RoleModule()
user_module = UserModule()


def get_role_name():
    role_id = user_module.get_user_role()
    role = role_module.get_single_role(role_id)
    if role:
        return role.name
    return None