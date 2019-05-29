from src.role.Role import Role
from src.role.RoleSet import RoleSet
from src.utils.singleton import Singleton
import psycopg2

role_set = RoleSet()


class RoleMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def update(self, role_obj):
        cursor = self.db.cursor()
        cursor.execute("UPDATE roles SET name=%s, pages=%s WHERE id=%s;", (role_obj.name, role_obj.pages, role_obj.id))
        self.db.commit()
        cursor.close()

    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM roles;")
        role_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for role_entry in role_entries:
            role_obj = role_set.find_by_all_fields(role_entry[cols_order.index("name")],
                                                   role_entry[cols_order.index("pages")])
            if not role_obj:
                role_obj = Role(role_entry[cols_order.index("name")],
                                role_entry[cols_order.index("pages")],
                                role_entry[cols_order.index("id")])
                role_set.add_role(role_obj)
        cursor.close()
