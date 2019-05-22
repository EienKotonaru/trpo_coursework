from src.student.Student import Student
from src.utils.singleton import Singleton
from src.student.StudentSet import StudentSet
import psycopg2

student_set = StudentSet()


class StudentMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, student_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO students (last_name, first_name, birth_date, gender, uuid, speciality, citizenship, " +
                       "groupname, enrollment, studying_type, grade_card, middle_name, dormitory, phone, address) " +
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                       (student_obj.last_name,
                        student_obj.first_name,
                        student_obj.birth_date,
                        student_obj.gender,
                        student_obj.uuid,
                        student_obj.speciality,
                        student_obj.citizenship,
                        student_obj.group,
                        student_obj.enrollment,
                        student_obj.studying_type,
                        student_obj.grade_card,
                        student_obj.middle_name,
                        student_obj.dormitory,
                        student_obj.phone,
                        student_obj.address))
        self.db.commit()
        student_obj.set_id(cursor.fetchone()[0])
        cursor.close()

    """def delete(self, user_obj):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM Criterias WHERE id=%s;", (user_obj.id,))
        self.db.commit()
        user_obj.id = cursor.lastrowid
        cursor.close()"""

    # Проверка, загружены ли все записи из БД (не относится к бизнес-логике)
    def load_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM students;")
        student_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for student_entry in student_entries:
            student_obj = student_set.find_by_uuid(student_entry[cols_order.index("uuid")])
            if not student_obj:
                student_obj = Student(student_entry[cols_order.index("last_name")],
                                      student_entry[cols_order.index("first_name")],
                                      student_entry[cols_order.index("birth_date")],
                                      student_entry[cols_order.index("gender")],
                                      student_entry[cols_order.index("uuid")],
                                      student_entry[cols_order.index("speciality")],
                                      student_entry[cols_order.index("citizenship")],
                                      student_entry[cols_order.index("group")],
                                      student_entry[cols_order.index("enrollment")],
                                      student_entry[cols_order.index("studying_type")],
                                      student_entry[cols_order.index("grade_card")],
                                      student_entry[cols_order.index("middle_name")],
                                      student_entry[cols_order.index("dormitory")],
                                      student_entry[cols_order.index("phone")],
                                      student_entry[cols_order.index("address")],
                                      )
                student_set.add_student(student_obj)
        cursor.close()
