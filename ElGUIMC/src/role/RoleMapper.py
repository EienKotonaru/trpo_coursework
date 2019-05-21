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

    """def insert(self, user_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id;", (user_obj.name, user_obj.weight, user_obj.measure, user_obj.group_id))
        self.db.commit()
        user_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    def delete(self, user_obj):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Criterias WHERE id=%s;", (user_obj.id,))
        self.db.commit()
        user_obj.id = cursor.lastrowid
        cursor.close()"""

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
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
