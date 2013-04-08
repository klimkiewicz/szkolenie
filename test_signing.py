import unittest

from werkzeug.datastructures import MultiDict

from signing import sign_args, check_signature


class SigningTestCase(unittest.TestCase):
    def testSignSimple(self):
        to_sign = {
            'user_id': 1,
        }
	k = MultiDict(to_sign)
        signed = sign_args(k)
        self.assertTrue(check_signature(signed))


if __name__ == '__main__':
    unittest.main()
