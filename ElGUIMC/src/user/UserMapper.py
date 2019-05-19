from src.user.User import User
from src.user.UserSet import UserSet
from src.utils.singleton import Singleton
from src.user.UserSet import UserSet
import psycopg2

user_set = UserSet()


class UserMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, criteria_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id;", (criteria_obj.name, criteria_obj.weight, criteria_obj.measure, criteria_obj.group_id))
        self.db.commit()
        criteria_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    def delete(self, user_obj):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Criterias WHERE id=%s;", (criteria_obj.id,))
        self.db.commit()
        criteria_obj.id = cursor.lastrowid
        cursor.close()

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users;")
        user_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for user_entry in user_entries:
            user_obj = user_set.find_by_all_fields(user_entry[cols_order.index("email")],
                                                           user_entry[cols_order.index("password")],
                                                           user_entry[cols_order.index("uuid")],
                                                           user_entry[cols_order.index("role_id")],)
            if not user_obj:
                user_obj = User(user_entry[cols_order.index("email")],
                                        user_entry[cols_order.index("password")],
                                        user_entry[cols_order.index("uuid")],
                                        user_entry[cols_order.index("role_id")],
                                        user_entry[cols_order.index("id")])
                user_set.add_user(user_obj)
        cursor.close()
