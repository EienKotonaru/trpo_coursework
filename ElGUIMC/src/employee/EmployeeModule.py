from src.utils.singleton import Singleton
from src.employee.Employee import Employee
from src.employee.EmployeeMapper import EmployeeMapper
from src.employee.EmployeeSet import EmployeeSet
import xml.etree.ElementTree as XmlTree
import dateutil.parser as date_parse
import json

employee_set = EmployeeSet()
employee_mapper = EmployeeMapper()


class EmployeeModule(metaclass=Singleton):
    def __init__(self):
        pass

    def import_from_json(self, json_content):
        for record in json_content.values():
            self.check_and_create(record)

    def check_and_create(self, json_record):
        employee = employee_set.find_by_uuid(json_record["Uid"])
        birthday_date = date_parse.parse(json_record["Birthday"]).date()
        if not employee:
            employee = Employee(json_record["Lastname"],
                                json_record["Firstname"],
                                birthday_date,
                                json_record["Gender"],
                                json_record["Uid"],
                                json_record["Middlename"],
                                None,
                                None,
                                self.empty_to_none(json_record['Degree']['Name']),
                                self.empty_to_none(json_record['Rank']['Name']))
            employee_mapper.insert(employee)
            employee_set.add_employee(employee)

    def empty_to_none(self, string):
        if string == "":
            string = None
        return string
    """def login(self, email, password):
        user_mapper.load_all()
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = user_set.find_by_email_password(email, hashed_password)
        if user:
            id_to_encrypt = str(user.id).zfill(16).encode("utf-8")
            des = DES.new(DES_KEY, DES.MODE_ECB)
            encrypted_id = des.encrypt(id_to_encrypt)
            hex_code = binascii.hexlify(encrypted_id)
            return hex_code.decode("utf-8")
        else:
            return "errror"

    def get_user_role(self):
        hex_code = request.cookies.get('userID')
        if hex_code is None:
            return None
        des = DES.new(DES_KEY, DES.MODE_ECB)
        user_bytes = hex_code.encode("utf-8")
        user_id = int(des.decrypt(binascii.unhexlify(user_bytes)))

        user_mapper.load_all()
        user = user_set.find_by_id(user_id)
        return user.role_id

        criteria = user_set.find(email, password)
        if not criteria:
            criteria = Criteria(name, weight, measure, group_id)
            criteria_mapper.insert(criteria)
            criteria_set.add_criteria(criteria)
            return criteria.id

    def get_criterias_by_group(self, group_id):
        criteria_mapper.load_all()
        criterias_by_group = criteria_set.criterias
        criterias_by_group = [obj for obj in criterias_by_group if int(obj.group_id) == int(group_id)]
        return criterias_by_group

    def remove_criteria(self, criteria_id):
        criteria_mapper.load_all()
        criteria_to_delete = criteria_set.find_by_id(criteria_id)
        if criteria_to_delete:
            criteria_mapper.delete(criteria_to_delete)
            criteria_set.remove_criteria(criteria_to_delete)"""
