from django.core.management.base import BaseCommand
import xml.etree.ElementTree
from base.models import Profile, Student
from base.utils import get_or_none


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def create_profile(self, person):
        gender = person.find('gender').attrib['name']
        gender_short = gender[0]
        profile, created = Profile.objects.get_or_create(
            uuid=person.attrib["uuid"],
            first_name=person.attrib["firstname"],
            last_name=person.attrib["lastname"],
            middle_name=person.attrib["middlename"],
            birthday=person.attrib["birthdate"],
            gender=gender_short
        )

        stage = person.find('stages').find('stage')
        group = stage.find('group')
        speciality = group.find('speciality')
        dormitory = person.find('dormitory').attrib['alias'].split('.')[1].title()

        current_student = get_or_none(Student, profile=profile)
        if not current_student and not stage.find('state').attrib['name'] == "Отчислен":
            student, created_st = Student.objects.get_or_create(
                profile=profile,
                speciality=speciality.attrib['speciality_code_formatted'],
                specialization=speciality.attrib['specialization_code'],
                group_abbr=group.attrib['abbr'],
                citizenship=person.find('citizenship').attrib['shortname'],
                enrollment_date=stage.attrib['start'],
                graduation_date=stage.attrib['end'],
                dormitory=dormitory
            )

    def handle(self, *args, **options):
        e = xml.etree.ElementTree.parse(options['filename']).getroot()
        for persons in e.findall('persons'):
            for person in persons.findall('person'):
                self.create_profile(person)
