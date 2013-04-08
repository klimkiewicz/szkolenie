import unittest

from passwords import get_password_for_database, check_password


class PasswordsTestCase(unittest.TestCase):
    MAX_PASSWORD_LENGTH = 100

    def testPasswordLengthOK(self):
        "Passwords stored in DB need to be at most 100 chars long."
        password_for_db = get_password_for_database('Test')
        self.assertTrue(len(password_for_db) <= self.MAX_PASSWORD_LENGTH)

        password_for_db = get_password_for_database('Test' * 2)
        self.assertTrue(len(password_for_db) <= self.MAX_PASSWORD_LENGTH)

    def testPossibleToSignIn(self):
        """
        It should be possible to sign in with the password provided during sign
        up.
        
        """
        password = 'This Is Some Password'
        password_for_db = get_password_for_database(password)
        self.assertTrue(check_password(password, password_for_db))

    def testWrongPasswordDoesntWork(self):
        "Wrong passwords don't work."
        password_good = 'This Is Some Password'
        password_bad = 'This is Some Other Password'
        password_for_db = get_password_for_database(password_good)
        self.assertFalse(check_password(password_bad, password_for_db))

    def testAppendingToPasswordDoesntWork(self):
        "Appending data to good password doesn't work."
        password = 'This Is Some Password'
        password_for_db = get_password_for_database(password)
        self.assertFalse(check_password(password + 'Extra', password_for_db))

    def testPasswordsLongerThanMaxDontWork(self):
        "Make sure password field limit doesn't affect the system."
        password = 'Some password' + 'A' * self.MAX_PASSWORD_LENGTH
        password_for_db = get_password_for_database(password)
        short_password = password[:self.MAX_PASSWORD_LENGTH]
        self.assertFalse(check_password(short_password, password_for_db))


if __name__ == '__main__':
    unittest.main()
