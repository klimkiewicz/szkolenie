import hashlib

salt = '123'


def get_password_for_database(password):
    hashed = hashlib.sha1(password)
    for i in range(3):
        hashed = hashlib.sha1(salt + hashed.hexdigest())
    return hashed.hexdigest()


def check_password(user_provided, from_database):
    return get_password_for_database(user_provided) == from_database


