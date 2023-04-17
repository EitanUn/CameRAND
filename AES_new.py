from Crypto.Cipher import AES


class AesNew:
    def __init__(self, key, nonce=None):
        self.key = key
        self.nonce = nonce

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        return cipher.encrypt(data)

    def decrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        return cipher.decrypt(data)
