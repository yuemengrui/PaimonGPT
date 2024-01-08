# *_*coding:utf-8 *_*
# @Author : YueMengRui
from passlib.context import CryptContext


class Crypto:

    def __init__(self):
        self.ctx = CryptContext(schemes=["pbkdf2_sha256"])

    def generate(self, secret):
        return self.ctx.hash(secret=secret)

    def verify(self, secret, hash):
        return self.ctx.verify(secret=secret, hash=hash)


crypto = Crypto()
