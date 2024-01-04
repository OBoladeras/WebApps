import hashlib

class PasswordEncryptor():
    def encrypt(self, password):
        sha3 = hashlib.sha3_256()
        sha3.update(password.encode('utf-8'))
        return sha3.hexdigest()
