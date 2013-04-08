import hashlib
import os
import sqlite3
import urllib
from contextlib import closing

from flask import abort, Flask, g, redirect, request
from werkzeug.datastructures import MultiDict

from dummy import send_email
from passwords import check_password, get_password_for_database
from signing import sign_args, check_signature
from templates import *


DATABASE = 'database.db'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)


# Database-related stuff

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    init_db()
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


# Sessions

@app.before_request
def set_sid():
    g.sid = get_session_id()
    if not g.sid:
        g.sid = get_new_sid()

@app.after_request
def after_request(response):
    if g.sid:
        response.set_cookie('SID', g.sid)
    else:
        response.set_cookie('SID', '', expires=0)
    return response

def get_session_id():
    if 'SID' in request.values:
        return request.values['SID']
    elif 'SID' in request.cookies:
        return request.cookies['SID']


def get_user_id():
    sid = get_session_id()
    if sid:
        sql = GET_USER % {
            'sid': sid,
        }
        cursor = g.db.cursor()
        cursor.execute(sql)
        user_id = cursor.fetchone()
        if user_id:
            return user_id[0]


def get_new_sid(user_id=None):
    sid = hashlib.md5(os.urandom(10)).hexdigest()

    if user_id:
        sql = ADD_SESSION % {
            'sid': sid,
            'user_id': user_id,
        }
    else:
        sql = ADD_SESSION_NO_USER % {
            'sid': sid,
        }

    cursor = g.db.cursor()
    cursor.executescript(sql)
    g.db.commit()

    return sid


def update_sid(sid, user_id):
    sql = UPDATE_SID % {
        'user_id': user_id,
        'sid': sid,
    }
    cursor = g.db.cursor()
    cursor.execute(sql)
    g.db.commit()


def login_user(user_id):
    sid = g.sid
    response = redirect('/')
    if not sid:
        sid = get_new_sid(user_id)
        response.set_cookie('SID', sid)
    else:
        update_sid(sid, user_id)

    return response


# Views

@app.route('/')
def index():
    user_id = get_user_id()
    if user_id:
        return 'logged in'
    else:
        return 'not logged in'


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return SIGN_UP
    else:
        # Assume there will be no duplicate entries here
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_for_db = get_password_for_database(password)

        c = g.db.cursor()

        sql = CREATE_USER % {
            'username': username,
            'password': password_for_db,
            'email': email,
        }
        c.executescript(sql)
        g.db.commit()

        sql = GET_USER_ID % {
            'username': username,
        }
        c.execute(sql)
        result = c.fetchone()

        to_sign = {
            'user_id': result[0],
        }
        signed = sign_args(MultiDict(to_sign))
        link = '/activate?' + urllib.urlencode(signed.to_dict(False))

        email = ACTIVATE_EMAIL % {
            'link': link,
            'email': email,
        }
        send_email(email)

        return 'Sign up complete.'


@app.route('/activate')
def activate():
    if check_signature(request.args):
        user_id = int(request.args['user_id'])

        sql = SET_ACTIVE % {
            'user_id': user_id,
        }
        c = g.db.cursor()
        c.executescript(sql)
        g.db.commit()
        
        return login_user(user_id)
    else:
        abort(400)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    sql = GET_PASSWORD % {
        'username': username,
    }

    cursor = g.db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        user_id, password_from_db = result

        if check_password(password, password_from_db):
            return login_user(user_id)

    abort(401)


@app.route('/account_delete')
def account_delete():
    user_id = get_user_id()
    if user_id:
        sql = DELETE_USER % {
            'user_id': user_id,
        }
        cursor = g.db.cursor()
        cursor.executescript(sql)
        g.db.commit()

        g.sid = None
        return redirect('/')
    else:
        abort(400)


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    user_id = get_user_id()

    if not user_id:
        abort(401)

    if request.method == 'GET':
        cursor = g.db.cursor()
        result = cursor.execute(GET_COMMENTS)
        comments = []
        for comment in result:
            comment = comment[0]
            comment_html = COMMENT % {
                'comment': comment,
            }
            comments.append(comment_html)
        comments_html = COMMENTS % {
            'comments': '\n'.join(comments),
        }
        return comments_html
    else:
        sql = CREATE_COMMENT % {
            'user_id': user_id,
            'comment': request.form['comment'],
        }
        cursor = g.db.cursor()
        cursor.executescript(sql)
        g.db.commit()

        return redirect('/comments')


if __name__ == '__main__':
    app.run()
