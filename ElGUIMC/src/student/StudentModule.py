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

    def get_single_student(self, student_id):
        student_mapper.load_all()
        return student_set.find_by_id(student_id)

    def set_additional_info(self, student_id, phone, address):
        student_mapper.load_all()
        student = student_set.find_by_id(student_id)
        student.phone, student.address = phone, address
        student_mapper.update(student)
        return

    def get_students_list(self):
        student_mapper.load_all()
        return student_set.students
