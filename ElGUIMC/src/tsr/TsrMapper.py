from src.utils.singleton import Singleton
from src.tsr.TsrSet import TsrSet
from src.tsr.Tsr import Tsr
import psycopg2

tsr_set = TsrSet()


class TsrMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, tsr_obj):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO tsrs (manufacturer, usage_since_year, type, student_id) VALUES (%s, %s, %s, %s) RETURNING id;",
            (tsr_obj.manufacturer, tsr_obj.usage_since_year, tsr_obj.type, tsr_obj.student_id))
        self.db.commit()
        tsr_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    def update(self, tsr_obj):
        cursor = self.db.cursor()
        cursor.execute("UPDATE tsrs SET manufacturer=%s, usage_since_year=%s, type=%s WHERE id=%s;",
                       (tsr_obj.manufacturer, tsr_obj.usage_since_year, tsr_obj.type, tsr_obj.id))
        self.db.commit()
        cursor.close()

    def delete(self, tsr_obj):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tsrs WHERE id=%s;", (tsr_obj.id,))
        self.db.commit()
        tsr_obj.id = cursor.lastrowid
        cursor.close()

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM tsrs;")
        tsr_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for tsr_entry in tsr_entries:
            tsr_obj = tsr_set.find_by_all_fields(tsr_entry[cols_order.index("manufacturer")],
                                                 tsr_entry[cols_order.index("usage_since_year")],
                                                 tsr_entry[cols_order.index("type")],
                                                 tsr_entry[cols_order.index("student_id")])
            if not tsr_obj:
                tsr_obj = Tsr(tsr_entry[cols_order.index("manufacturer")],
                              tsr_entry[cols_order.index("usage_since_year")],
                              tsr_entry[cols_order.index("type")],
                              tsr_entry[cols_order.index("student_id")],
                              tsr_entry[cols_order.index("id")])
                tsr_set.add_tsr(tsr_obj)
        cursor.close()
