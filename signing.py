from hashlib import sha1

from werkzeug.datastructures import MultiDict

KEY = 'AnMoPlUxE'


def signature(args):
    tokens = []
    for key in args:
        if key != 'signature':
            tokens.append(key)
            tokens.extend([str(item) for item in args.getlist(key)])
    tokens.append(KEY)
    line = ''.join(tokens)
    return sha1(line).hexdigest()


def sign_args(args):
    result = MultiDict(args)
    result['signature'] = signature(args)
    return result


def check_signature(args):
    return signature(args) == args['signature']