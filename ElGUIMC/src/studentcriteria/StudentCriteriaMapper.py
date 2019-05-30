from src.utils.singleton import Singleton
from src.studentcriteria.StudentCriteria import StudentCriteria
from src.studentcriteria.StudentCriteriaSet import StudentCriteriaSet
import psycopg2

student_criteria_set = StudentCriteriaSet()


class StudentCriteriaMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, student_criteria_obj):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO students_criterias (student_id, criteria_id, weight) VALUES (%s, %s, %s) RETURNING id;",
            (student_criteria_obj.student_id, student_criteria_obj.criteria_id, student_criteria_obj.weight))
        self.db.commit()
        student_criteria_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    def update(self, student_criteria_obj):
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE students_criterias SET student_id=%s, criteria_id=%s, weight=%s WHERE id=%s;",
            (student_criteria_obj.student_id, student_criteria_obj.criteria_id, student_criteria_obj.weight, student_criteria_obj.id))
        self.db.commit()
        cursor.close()

    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM students_criterias;")
        student_criteria_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for student_criteria_entry in student_criteria_entries:
            student_criteria_obj = student_criteria_set.find(student_criteria_entry[cols_order.index("student_id")],
                                                             student_criteria_entry[cols_order.index("criteria_id")],
                                                             student_criteria_entry[cols_order.index("weight")])
            if not student_criteria_obj:
                student_criteria_obj = StudentCriteria(student_criteria_entry[cols_order.index("student_id")],
                                                       student_criteria_entry[cols_order.index("criteria_id")],
                                                       student_criteria_entry[cols_order.index("weight")],
                                                       student_criteria_entry[cols_order.index("id")])
                student_criteria_set.add_student_criteria(student_criteria_obj)
        cursor.close()
