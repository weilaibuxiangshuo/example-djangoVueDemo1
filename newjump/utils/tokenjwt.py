# -*- coding:utf-8 -*-
from newjump import settings

import jwt

class Token(object):
    def __init__(self):
        self.key = settings.SECRET_KEY

    def encodejwt(self,data):
        return jwt.encode({"username":data}, self.key, algorithm='HS256').decode("utf8")

    def decodejwt(self,token):
        if isinstance(token,bytes):
            data = jwt.decode(token,self.key, algorithm='HS256')
            return data
        else:
            newT = token.encode()
            data = jwt.decode(newT,self.key, algorithm='HS256')
            return data
