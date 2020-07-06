# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver,URLPattern,RoutePattern,RegexPattern
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.core.cache import cache
from collections.abc import Iterable
import re,json

import dns.resolver

from .models import User,Jump

from utils.resultful import Resf as ref
from utils.tokenjwt import Token
from .toolcache import Cache

class NewMethodMiddle(MiddlewareMixin):
    urlList = set()
    def process_request(self,request):
        # print(request.POST)
        whiteUrl = ["/api/login/"]
        newPath = request.META.get("PATH_INFO",None)
        print(newPath,"newpat")
        if newPath not in whiteUrl:
            allUrl = import_string(settings.ROOT_URLCONF)
            # 获取所有url
            self.get_url(allUrl.urlpatterns,"")
            # print("---",self.urlList)
            # 判断是否在url里面
            result = self.isRelease(self.urlList,newPath)
            print(result,"結果")
            if result:
                newAuth = request.META.get("HTTP_AUTHORIZATION",None)
                #判断是否有token
                # print("token",newAuth)
                if not newAuth:
                    return JsonResponse(ref.code(401))
                cacheAuth = cache.get(newAuth)
                #判断是否有这个token
                if not cacheAuth:
                    return JsonResponse(ref.code(401))
                try:
                    #判断是否有这个用户
                    userAuth = Token().decodejwt(newAuth)["username"]
                    # print(userAuth,"userauth")
                except Exception as e:
                    return JsonResponse(ref.code(401))
                if not userAuth:
                    return JsonResponse(ref.code(401))
            else:
                callBackRes = self.resolveUrl(request)
                print(callBackRes,"call")
                if callBackRes=="error":
                    return HttpResponse(status=403)
                else:
                    return HttpResponse(callBackRes)


    @classmethod
    def get_url(cls,data,parentPath=""):
        for m in data:
            if isinstance(m,URLPattern):
                if str(m.pattern)==".*":
                    continue
                if not parentPath:
                    if isinstance(m.pattern,RegexPattern):
                        print(m.pattern,"1111")
                        reg1 = re.compile("[\^](.*)[\$]")
                        result = reg1.findall(str(m.pattern))
                        cls.urlList.add(result[0])
                    else:
                        result = str(m.pattern)
                        cls.urlList.add(result)
                else:
                    if isinstance(m.pattern,RegexPattern):
                        reg1 = re.compile("[\^](.*)[\$]")
                        result = reg1.findall(str(m.pattern))
                        newRes = str(parentPath)+result[0]
                        cls.urlList.add(newRes)
                    else:
                        newRes = str(parentPath)+str(m.pattern)
                        cls.urlList.add(newRes)
            elif isinstance(m,URLResolver):
                if hasattr(m,"url_patterns"):
                    cls.get_url(m.url_patterns,m.pattern)
        return True

    @classmethod
    def isRelease(cls,urlList,path):
        newPath = path[1:]
        isTemp = False
        for one in list(urlList):
            pattern = eval(repr(one))
            regEx = re.compile(pattern)
            result = regEx.match(newPath)
            if result:
                isTemp = True
        if isTemp:
            return True
        else:
            return False

    @classmethod
    def resolveUrl(cls,request,num=3):
        dict = {
            1:"HTTP_HOST",
            2:"HTTP_REFERER",
            3:["HTTP_HOST","HTTP_REFERER"]
        }
        # print("dict",dict,type(num),num)
        if int(num)==3:
            getInfo = request.META.get(dict[int(num)][0],"")
            if not getInfo:
                getInfo = request.META.get(dict[int(num)][1], "")
        else:
            getInfo = request.META.get(dict[int(num)], "")
        print(getInfo,"---")
        getInfo="www.blr424.com"
        if getInfo:
            getInfoSlice = re.split("\.",str(getInfo))[-2:]
            newUrl = "www."+getInfoSlice[0]+"."+getInfoSlice[1]
            jumpCache = cache.get("jumpObj","")
            if not jumpCache:
                Cache().set()
                jumpCache = cache.get("jumpObj","")
            try:
                getJump = jumpCache.filter(name=newUrl)
            except Exception as e:
                return "error"
            if getJump:
                oneJump = getJump.first()
                if oneJump.is_jump:
                    return oneJump.jumptarget
                else:
                    try:
                        res = dns.resolver.query(newUrl, "A")
                    except Exception as e:
                        return "error"
                    resList = []
                    for n in res.response.answer:
                        resList.append(str(n[0])[0:-1])
                    if oneJump.relationship.username in resList:
                        return oneJump.relationship.target
        return "error"