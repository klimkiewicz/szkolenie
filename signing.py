from hashlib import sha1
SECRET_KEY = 'asdha1293718u3j1d01d19dj120jd1212741829d'

def sign_args(args):
	signature = str(args.to_dict()) + SECRET_KEY
	for i in range(100):
	    signature = sha1(signature).hexdigest()
	args['signature'] = signature
	return args


def check_signature(args):
    signature = args.pop('signature', None)
    if not signature:
        return False
    reference = str(args.to_dict()) + SECRET_KEY
    for i in range(100):
        reference = sha1(reference).hexdigest()
    return signature == reference
