from django.core.management.base import BaseCommand
import json
from base.models import Profile, Staff
from base.utils import get_or_none
import dateutil.parser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def create_profile(self, record):
        birthday_date = dateutil.parser.parse(record["Birthday"]).date()
        profile, created = Profile.objects.get_or_create(
            uuid=record["Uid"],
            first_name=record["Firstname"],
            last_name=record["Lastname"],
            middle_name=record["Middlename"],
            birthday=birthday_date,
            gender=record['Gender'].upper()
        )

        current_staff = get_or_none(Staff, profile=profile)
        if not current_staff:
            staff, created_st = Staff.objects.get_or_create(
                profile=profile,
                struct_name=record['Employment'][0]['Struct']['Name'],
                profession=record['Employment'][0]['Profession']['Name'],
                academic_degree=self.empty_to_null(record['Degree']['Name']),  # ученая степень
                academic_title=self.empty_to_null(record['Rank']['Name'])  # ученое звание
            )

    def empty_to_null(self, string):
        if string == "":
            string = None
        return string

    def handle(self, *args, **options):
        with open(options['filename'], "r") as read_file:
            data = json.load(read_file)
            for record in data.values():
                self.create_profile(record)
