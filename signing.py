import hashlib
SECRET = "asdadas ewr34552342 52w t54t 2"

def sign_args(args):
    h = hashlib.new('sha256')
    argstr = str(args.to_dict())
    for i in range(500):
        hsh = h.update(argstr+SECRET)
    args['chksum'] = h.hexdigest()
    return args


def check_signature(args):
    chk = args.pop('chksum')
    argsout = sign_args(args)
    if chk == argsout['chksum']:
        return True
    else:
        return False
