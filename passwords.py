import hashlib
SECRET_KEY = 'asdassada89yr87qy452oh3874434939804298KROIW9J8'

def get_password_for_database(password):
    password = SECRET_KEY+password
    h = hashlib.new('sha224')
    for i in range(500):
        password = h.update(password)
        password = h.hexdigest()
    return password


def check_password(user_provided, from_database):
    user_provided = get_password_for_database(user_provided)
    return user_provided == from_database
