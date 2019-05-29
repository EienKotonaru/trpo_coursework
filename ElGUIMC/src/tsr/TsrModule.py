from src.utils.singleton import Singleton
from src.tsr.TsrSet import TsrSet
from src.tsr.Tsr import Tsr
from src.tsr.TsrMapper import TsrMapper

tsr_set = TsrSet()
tsr_mapper = TsrMapper()


class TsrModule(metaclass=Singleton):
    def __init__(self):
        pass

    def create_tsr(self, manufacturer, usage_since_year, type, student_id):
        tsr_mapper.load_all()
        tsr = Tsr(manufacturer, usage_since_year, type, student_id)
        tsr_mapper.insert(tsr)
        tsr_set.add_tsr(tsr)

    def update_tsr(self, manufacturer, usage_since_year, type, id):
        tsr_mapper.load_all()
        tsr = tsr_set.find_by_id(id)
        tsr.manufacturer, tsr.usage_since_year, tsr.type = manufacturer, usage_since_year, type
        tsr_mapper.update(tsr)

    def get_tsrs_list(self):
        tsr_mapper.load_all()
        return tsr_set.tsrs

    def get_tsrs_by_student(self, student_id):
        tsr_mapper.load_all()
        tsrs_by_student = tsr_set.tsrs
        tsrs_by_student = [obj for obj in tsrs_by_student if int(obj.student_id) == int(student_id)]
        return tsrs_by_student

    def remove_tsr(self, tsr_id):
        tsr_mapper.load_all()
        tsr_to_delete = tsr_set.find_by_id(tsr_id)
        if tsr_to_delete:
            tsr_mapper.delete(tsr_to_delete)
            tsr_set.remove_tsr(tsr_to_delete)
