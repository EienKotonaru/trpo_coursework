from src.employee.Employee import Employee
from src.utils.singleton import Singleton
from src.employee.EmployeeSet import EmployeeSet
import psycopg2

employee_set = EmployeeSet()


class EmployeeMapper(metaclass=Singleton):
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            user="guimc",
            password="coursework",
            dbname="trpo_course"
        )

    def insert(self, employee_obj):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO employees (last_name, first_name, birth_date, gender, uuid, " +
                       "phone, work_auditory, title, degree) " +
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                       (employee_obj.last_name,
                        employee_obj.first_name,
                        employee_obj.birth_date,
                        employee_obj.gender,
                        employee_obj.uuid,
                        employee_obj.phone,
                        employee_obj.work_auditory,
                        employee_obj.title,
                        employee_obj.degree))
        self.db.commit()
        employee_obj.set_id(cursor.fetchone()[0])
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
        cursor.execute("SELECT * FROM employees;")
        employee_entries = cursor.fetchall()
        cols_order = [col[0] for col in cursor.description]

        for employee_entry in employee_entries:
            employee_obj = employee_set.find_by_uuid(employee_entry[cols_order.index("uuid")])
            if not employee_obj:
                employee_obj = Employee(employee_entry[cols_order.index("last_name")],
                                        employee_entry[cols_order.index("first_name")],
                                        employee_entry[cols_order.index("birth_date")],
                                        employee_entry[cols_order.index("gender")],
                                        employee_entry[cols_order.index("uuid")],
                                        employee_entry[cols_order.index("phone")],
                                        employee_entry[cols_order.index("work_auditory")],
                                        employee_entry[cols_order.index("title")],
                                        employee_entry[cols_order.index("degree")]
                                        )
                employee_set.add_employee(employee_obj)
        cursor.close()
