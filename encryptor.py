import os
from Crypto import Random
from Crypto.Cipher import AES

class AES_Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, m, key, key_size=256):
        m = self.pad(m)
        iv = Random.new().read(AES.block_size)
        c = AES.new(key, AES.MODE_GCM, iv)
        return iv + c.encrypt(m)

    def encryptFile(self, filepath):
        with open(filepath, 'rb') as uf:
            plain = uf.read()
        encrypted = self.encrypt(plain, self.key)
        with open(filepath + ".enc", 'wb') as uf:
            uf.write(encrypted)
        os.remove(filepath)

    def decrypt(self, cipher, key):
        iv = cipher[:AES.block_size]
        c = AES.new(key, AES.MODE_GCM, iv)
        plain = c.decrypt(cipher[AES.block_size:])
        return plain.rstrip(b"\0")

    def decryptFile(self, filepath, file):
        with open(filepath + file, 'rb') as ef:
            cipher = ef.read()
        dec = self.decrypt(cipher, self.key)
        with open('static/private_pic/' + file[:-4], 'wb') as output:
            output.write(dec)

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = AES_Encryptor(key)
