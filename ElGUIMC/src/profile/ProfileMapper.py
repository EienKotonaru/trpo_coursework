from src.profile.Profile import Profile
from src.utils.singleton import Singleton
from src.profile.ProfileSet import ProfileSet
import psycopg2

profile_set = ProfileSet()


class ProfileMapper(metaclass=Singleton):
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
        cursor.execute("SELECT * FROM profiles;")
        profile_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for profile_entry in profile_entries:
            profile_obj = profile_set.find_by_uuid(profile_entry[cols_order.index("uuid")])
            if not profile_obj:
                profile_obj = Profile(profile_entry[cols_order.index("last_name")],
                                      profile_entry[cols_order.index("first_name")],
                                      profile_entry[cols_order.index("birth_date")],
                                      profile_entry[cols_order.index("gender")],
                                      profile_entry[cols_order.index("uuid")],
                                      profile_entry[cols_order.index("phone")],
                                      profile_entry[cols_order.index("middle_name")]
                                      )
                profile_set.add_profile(profile_obj)
        cursor.close()
