import logging
import os
import tempfile
import unittest
import urllib

import app
from passwords import get_password_for_database
from signing import sign_args
from templates import *


def create_user(username='test', password='test', email='test@example.com',
                active=False):
    app.init_db()

    password = get_password_for_database(password)

    if active:
        sql = CREATE_ACTIVE_USER
    else:
        sql = CREATE_USER

    sql = sql % {
        'username': username,
        'password': password,
        'email': email,
    }

    db = app.connect_db()
    db.executescript(sql)
    db.commit()


class GeneralTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def testGetIndex(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def testSignUp(self):
        response = self.app.get('/sign_up')
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/sign_up', data={
            'username': 'test',
            'password': 'test',
            'email': 'test@example.com',
        })
        self.assertEqual(response.status_code, 200)

    def testActivate(self):
        create_user()

        signed = sign_args({
            'user_id': 1,
        })
        link = '/activate?' + urllib.urlencode(signed)

        response = self.app.get(link)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'logged in')

    def testLogin(self):
        create_user(active=True)

        response = self.app.get('/')
        self.assertEqual(response.data, 'not logged in')

        response = self.app.post('/login', data={
            'username': 'test',
            'password': 'test',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')

        response = self.app.get('/')
        self.assertEqual(response.data, 'logged in')

    def testDeleteAccount(self):
        create_user(active=True)

        response = self.app.post('/login', data={
            'username': 'test',
            'password': 'test',
        })

        response = self.app.get('/account_delete')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')

        response = self.app.get('/')
        self.assertEqual(response.data, 'not logged in')

        response = self.app.post('/login', data={
            'username': 'test',
            'password': 'test',
        })
        self.assertEqual(response.status_code, 401)

    def testComments(self):
        create_user(active=True)

        response = self.app.post('/login', data={
            'username': 'test',
            'password': 'test',
        })

        response = self.app.post('/comments', data={
            'comment': 'This is test comment',
        })
        self.assertEqual(response.status_code, 302)

        response = self.app.get('/comments')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('This is test comment' in response.data)


if __name__ == '__main__':
    unittest.main()
