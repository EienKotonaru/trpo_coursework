import csv

from src.user.User import User
from src.utils.singleton import Singleton
from src.user.UserMapper import UserMapper
from Crypto.Cipher import DES
import hashlib
from src.user.UserSet import UserSet
import binascii
from flask import url_for, request, redirect

user_set = UserSet()
user_mapper = UserMapper()
DES_KEY = b"eguimc19"


class UserModule(metaclass=Singleton):
    def __init__(self):
        pass

    # Проверка на основе сведений о предметной области (бизнес-логика)
    def register(self, email, password, username_ais, password_ais):
        with open("ldap.csv", 'r') as file:
            reader = csv.reader(file)
            uuid = None
            for row in reader:
                if row[0] == username_ais and row[1] == password_ais:
                    uuid = row[2]
                    break

        if uuid:
            user_mapper.load_all()
            hashed_password = hashlib.sha256(password.encode('utf8')).hexdigest()
            user = user_set.find_by_all_fields(email, hashed_password, uuid, 2) #TODO
            if not user:
                user = User(email, hashed_password, 1, 1) #TODO
                user_mapper.insert(user)

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
            return "error"

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



        """criteria = user_set.find(email, password)
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
