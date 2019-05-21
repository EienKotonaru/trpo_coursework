from src.utils.singleton import Singleton
from src.profile.ProfileMapper import ProfileMapper
from src.profile.ProfileSet import ProfileSet

profile_set = ProfileSet()
profile_mapper = ProfileMapper()


class UserModule(metaclass=Singleton):
    def __init__(self):
        pass

    # Проверка на основе сведений о предметной области (бизнес-логика)
    """def register(self, email, password):
        sha = hashlib.sha256(password.encode('utf8')).hexdigest()
        print(sha)

    def login(self, email, password):
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
