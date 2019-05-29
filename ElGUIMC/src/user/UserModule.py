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

    def register(self, email, password, profile_id, role_id):
        if profile_id and role_id:
            user_mapper.load_all()
            user = user_set.find_by_profile(profile_id)
            if not user:
                hashed_password = hashlib.sha256(password.encode('utf8')).hexdigest()
                user = user_set.find_by_all_fields(email, hashed_password, profile_id, role_id)
                if not user:
                    user = User(email, hashed_password, profile_id, role_id)
                    user_mapper.insert(user)
            return "User is already registered"

    def ldap_login(self, username_ais, password_ais):
        with open("ldap.csv", 'r') as file:
            reader = csv.reader(file)
            uuid = None
            for row in reader:
                if row[0] == username_ais and row[1] == password_ais:
                    uuid = row[2]
                    break
        return uuid

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

    def get_user(self):
        hex_code = request.cookies.get('userID')
        if hex_code is None:
            return None
        des = DES.new(DES_KEY, DES.MODE_ECB)
        user_bytes = hex_code.encode("utf-8")
        user_id = int(des.decrypt(binascii.unhexlify(user_bytes)))
        return user_set.find_by_id(user_id)
