from src.utils.singleton import Singleton
from src.criteria.CriteriaSet import CriteriaSet
from src.criteria.Criteria import Criteria
import psycopg2

criteria_set = CriteriaSet()


class CriteriaMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, criteria_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO Criterias (name, weight, measure, group_id) VALUES (%s, %s, %s, %s) RETURNING id;", (criteria_obj.name, criteria_obj.weight, criteria_obj.measure, criteria_obj.group_id))
        self.db.commit()
        criteria_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    def delete(self, criteria_obj):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Criterias WHERE id=%s;", (criteria_obj.id,))
        self.db.commit()
        criteria_obj.id = cursor.lastrowid
        cursor.close()

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM Criterias;")
        criteria_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for criteria_entry in criteria_entries:
            criteria_obj = criteria_set.find_by_all_fields(criteria_entry[cols_order.index("name")],
                                                           criteria_entry[cols_order.index("weight")],
                                                           criteria_entry[cols_order.index("measure")],
                                                           criteria_entry[cols_order.index("group_id")],)
            if not criteria_obj:
                criteria_obj = Criteria(criteria_entry[cols_order.index("name")],
                                        criteria_entry[cols_order.index("weight")],
                                        criteria_entry[cols_order.index("measure")],
                                        criteria_entry[cols_order.index("group_id")],
                                        criteria_entry[cols_order.index("id")])
                criteria_set.add_criteria(criteria_obj)
        cursor.close()
