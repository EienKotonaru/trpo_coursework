from src.utils.singleton import Singleton
from src.group.GroupSet import GroupSet
from src.group.Group import Group
import psycopg2

group_set = GroupSet()


class GroupMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, group_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO groups (name, description) VALUES (%s, %s) RETURNING id;", (group_obj.name, group_obj.description))
        self.db.commit()
        group_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM groups;")
        group_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for group_entry in group_entries:
            group_obj = group_set.find(group_entry[cols_order.index("name")],
                                       group_entry[cols_order.index("description")])
            if not group_obj:
                group_obj = Group(group_entry[cols_order.index("name")],
                                  group_entry[cols_order.index("description")],
                                  group_entry[cols_order.index("id")])
                group_set.add_group(group_obj)
        cursor.close()

    # Проверка, загружена ли запись ранее (не относится к бизнес-логике)
    def load(self, group_id):
        group_obj = group_set.find_by_id(group_id)
        if not group_obj:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM groups WHERE id=(%s);", group_id)
            group_entry = cursor.fetchone()

            cols_order = [col[0] for col in cursor.description]
            group_obj = Group(group_entry[cols_order.index("name")],
                              group_entry[cols_order.index("description")],
                              group_entry[cols_order.index("id")])
            group_set.add_group(group_obj)
            cursor.close()