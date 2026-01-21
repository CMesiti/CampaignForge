from argon2 import PasswordHasher, exceptions

def hash_pass(pswd):
    ph = PasswordHasher()
    hash = ph.hash(pswd)
    return hash

def check_pass(entered_pswd, hash):
    ph = PasswordHasher()
    try:
        ph.verify(hash, entered_pswd)
        return True, None
    except exceptions.VerifyMismatchError as e:
        return False, e