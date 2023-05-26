"""
Author: Eitan Unger
Date: 18/04/23
description: A small class to create a persistent AES cipher object that doesn't require any command between actions
"""
import logging
from Crypto.Cipher import AES


class AesNew:
    """
    pyCryptoDome's AES class wrapped in a class to hold the key and nonce
    """
    def __init__(self, key, nonce=None):
        """
        init for my AES cipher object
        """
        self.key = key
        self.nonce = nonce
        logging.debug("AES: created new cipher object")

    def encrypt(self, data):
        """
        AES encrypt function
        :param data: data to encrypt
        :return: AES encrypted data
        """
        logging.debug("AES: encrypting message %s" % data)
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        return cipher.encrypt(data)

    def decrypt(self, data):
        """
        AES decrypt function
        :param data: AES encrypted data
        :return: plaintext data (in bytes)
        """
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        res = cipher.decrypt(data)
        logging.debug("AES: decrypted message %s" % res)
        return res
