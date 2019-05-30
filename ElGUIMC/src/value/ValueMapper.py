from src.utils.singleton import Singleton
from src.value.ValueSet import ValueSet
from src.value.Value import Value
import psycopg2
from time import strftime

value_set = ValueSet()


class ValueMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, value_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO CriteriaValues (value, assignment_time, criteria_id, student_id) VALUES (%s, %s, %s, %s) RETURNING id;", (value_obj.value, strftime("%Y-%m-%d %H:%M:%S", value_obj.assignment_time), value_obj.criteria_id, value_obj.student_id))
        self.db.commit()
        value_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM CriteriaValues;")
        value_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for value_entry in value_entries:
            value_obj = value_set.find_by_all_fields(value_entry[cols_order.index("value")],
                                                     value_entry[cols_order.index("assignment_time")],
                                                     value_entry[cols_order.index("criteria_id")],
                                                     value_entry[cols_order.index("student_id")])
            if not value_obj:
                value_obj = Value(value_entry[cols_order.index("value")],
                                  value_entry[cols_order.index("assignment_time")],
                                  value_entry[cols_order.index("criteria_id")],
                                  value_entry[cols_order.index("student_id")],
                                  value_entry[cols_order.index("id")])
                value_set.add_value(value_obj)
        cursor.close()

