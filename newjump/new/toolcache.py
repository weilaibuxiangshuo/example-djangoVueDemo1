# -*- coding:utf-8 -*-
from django.core.cache import cache

from .models import User,Jump

class Cache(object):
    def set(self):
        userObj = User.objects.all()
        cache.set("userObj",userObj,60*10)
        jumpObj = Jump.objects.all()
        cache.set("jumpObj",jumpObj,60*10)

    def setUser(self):
        userObj = User.objects.all()
        cache.set("userObj",userObj,60*10)

    def setJump(self):
        jumpObj = Jump.objects.all()
        cache.set("jumpObj",jumpObj,60*10)
