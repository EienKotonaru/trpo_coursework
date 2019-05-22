from src.utils.singleton import Singleton
from src.student.Student import Student
from src.student.StudentMapper import StudentMapper
from src.student.StudentSet import StudentSet
import xml.etree.ElementTree as XmlTree

student_set = StudentSet()
student_mapper = StudentMapper()


class StudentModule(metaclass=Singleton):
    def __init__(self):
        pass

    def import_from_xml(self, xml_content):
        e = XmlTree.fromstring(xml_content)
        for persons in e.findall('persons'):
            for person in persons.findall('person'):
                self.check_and_create(person)

    def check_and_create(self, xml_record):
        student = student_set.find_by_uuid(xml_record.attrib["uuid"])
        stage = xml_record.find('stages').find('stage')
        if not student and not stage.find('state').attrib['name'] == "Отчислен":
            group = stage.find('group')
            speciality = group.find('speciality')
            gender = None
            if xml_record.find('gender').attrib['name'][0] == 'М':
                gender = 'm'
            elif xml_record.find('gender').attrib['name'][0] == 'Ж':
                gender = 'f'
            student = Student(xml_record.attrib["lastname"],
                              xml_record.attrib["firstname"],
                              xml_record.attrib["birthdate"],
                              gender,
                              xml_record.attrib["uuid"],
                              group.find('speciality').attrib['speciality_code_formatted'],
                              xml_record.find('citizenship').attrib['shortname'],
                              group.attrib['abbr'],
                              stage.attrib['start'],
                              stage.find('studytype').attrib['name'],
                              stage.attrib['card_number'],
                              xml_record.attrib["middlename"],
                              xml_record.find('dormitory').attrib['alias'].split('.')[1].title())
            student_mapper.insert(student)
            student_set.add_student(student)


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
