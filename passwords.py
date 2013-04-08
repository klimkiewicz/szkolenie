from hashlib import sha1

def get_password_for_database(password):
    for i in range(100):
        password = str(sha1(password).hexdigest())
    return password


def check_password(user_provided, from_database):
    return get_password_for_database(user_provided) == from_database
