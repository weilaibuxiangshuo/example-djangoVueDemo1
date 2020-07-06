from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.utils.decorators import method_decorator
import json,re,time

from .models import User,Jump
from .toolcache import Cache
from utils.resultful import Resf as ref
from utils.tokenjwt import Token




class MyException(Exception):
    def __init__(self,newError):
        self.newError = newError

class Login(View):
    """
    用户登陆
    """
    def post(self,request):
        # return JsonResponse(ref.set(400, "用户或密码错误"))
        userInfo = json.loads(request.POST.get("data"))
        print(userInfo,"uuuuuu")
        isUser = authenticate(username=userInfo["username"],password=userInfo["password"])
        if isUser:
            login(request,isUser)
            tk = Token().encodejwt(isUser.username)
            cache.set(str(tk),isUser.username,60*60)
            data = {
                "token":tk
            }
            data.update(ref.code(200))
            return JsonResponse(data)
        else:
            return JsonResponse(ref.set(400,"用户或密码错误"))


class UserInfo(View):
    def get(self,request):
        # print(request.user,"user")
        getUser = User.objects.filter(username=request.user).first()
        if not getUser:
            return JsonResponse(ref.code(401))
        if getUser.is_superuser and getUser.mode == None:
            roles = 'admin'
        else:
            roles = 'subuser'
        data = {
            "userid":getUser.id,
            "username":getUser.username,
            "roles":roles
        }
        data.update(ref.code(200))
        return JsonResponse(data)


class GetUser(View):
    """
    用户返回数据
    """
    def get(self,request,page,size):
        if all([page,size]):
            page=int(page)
            size=int(size)
            startPage = (page-1)*size
            endPage = page*size
            search = request.GET.get("search", None)
            if search:
                allUsers = User.objects.all().exclude(mode=None).order_by('-id').filter(username=search)
            else:
                allUsers=User.objects.all().exclude(mode=None).order_by('-id')[startPage:endPage]
            newL = []
            for us in allUsers:
                one = {
                    "id":us.id,
                    "username":us.username,
                    "num":us.number,
                    "mode":list(us.mode),
                    "target":us.target,
                    "isSuperUser":us.is_superuser,
                }
                newL.append(one)
            data = {
                "data": newL,
                "total":User.objects.exclude(mode=None).count(),
            }
            data.update(ref.code(200))
            return JsonResponse(data)
        else:
            return JsonResponse(ref.code(403))

class MgUser(View):
    """
    用户添加
    """
    def post(self,request):
        data = request.POST.get("data",None)
        if data is None:
            return JsonResponse(ref.code(400))
        userInfo=json.loads(data)
        try:
            getUsers = User.objects.exclude(mode=None).filter(username=userInfo['username'])
            newMode = userInfo['mode'] if len(userInfo['mode']) == 1 else None
            newSuperUser = True if len(userInfo['isSuperUser']) == 1 else False
            newPassword = userInfo['password'] if len(userInfo['password']) else None
        except Exception as e:
            return JsonResponse(ref.code(400))
        if getUsers:
            # print(getUsers.first().mode,"---",newMode)
            # print(type(getUsers.first().mode),"---",type(str(newMode)))
            oneUser = getUsers.first()
            isFunc = oneUser.mode == str(newMode[0])
            _dict1 = {
                "password":make_password(newPassword.strip()),
                "target":userInfo['target'],
                "mode":newMode[0],
                "number":int(userInfo['num']),
                "is_superuser":newSuperUser,
                "is_staff": True,
                "is_active": True,
            }
            if newPassword is None and newSuperUser:
                _dict1.pop("password","error")
            elif not newSuperUser:
                _dict1["password"]=make_password(userInfo['username'])
            if not isFunc:
                val = int(newMode[0])
                self.UserProcess(oneUser, val)
            #模式对应的jump目标要变动
            getUsers.update(**_dict1)
            newOneUser = getUsers.first()
            if int(newMode[0]) in [1,5]:
                newOneUser.jump_target.all().update(jumptarget=newOneUser.target)
            Cache().set()
            return JsonResponse(ref.code(202))
        else:
            _dict2 = {
                "username":userInfo['username'],
                "password":make_password(newPassword.strip()),
                "target":userInfo['target'],
                "mode":newMode[0],
                "number":int(userInfo['num']),
                "is_superuser":newSuperUser,
                "is_staff":True,
                "is_active":True,
            }
            if not newSuperUser:
                _dict2["password"]=make_password(userInfo['username'])
            User.objects.create(**_dict2)
            Cache().set()
            return JsonResponse(ref.code(201))

    @classmethod
    def UserProcess(cls,oneUser,val):
        newdict = {
            1: {"is_jump":False},
            2: {"is_jump":False},
            5: {"is_jump":True},
            6: {"is_jump":True},
        }
        JumpObjs =oneUser.jump_target.all()
        for one in JumpObjs:
            one.is_jump=newdict[val]["is_jump"]
        return None



class DelUser(View):
    """
    用户删除
    """
    def delete(self,request):
        delData =request.body.decode("utf8")
        delList = json.loads(delData)
        if isinstance(delList,list):
            for i in delList:
                User.objects.filter(id=i["id"]).delete()
        Cache().set()
        return JsonResponse(ref.code(204))

class GetData(View):
    """
    Jump对应的用户信息获取
    """
    def get(self,request):
        userId = request.GET.get("userid",None)
        if userId:
            newData = User.objects.exclude(mode=None).filter(id=int(userId))
        else:
            newData = User.objects.exclude(mode=None).all()
        newList = []
        for one in newData:
            _dict = {
                "id":one.id,
                "username":one.username,
                "num":one.number,
                "target":one.target,
                "mode":list(one.mode),
                "jumpnum":len(one.jump_target.all()),
                "jumplist":"",
            }
            newList.append(_dict)
        data = {
            "data":newList,
        }
        data.update(ref.code(200))
        return JsonResponse(data)

class JpData(View):
    """
    Jump添加数据
    """
    def post(self,request):
        dataP = request.POST.get("data")
        data= json.loads(dataP)
        newUser=User.objects.filter(id=data["id"]).first()
        numFunc=int(data["mode"])
        try:
            result = self.dataStorage(newUser, data,numFunc)
        except Exception as e:
            Cache().set()
            return JsonResponse(e.newError)
        if result:
            Cache().set()
            return JsonResponse(ref.code(201))

    @classmethod
    def dataStorage(cls,newUser,data,num):
        msgList = []
        #"1"DNS多对一 "2" DNS多对多 "5" SQL多对一" 6" SQL多对多
        regExJump = {
            1: {"jumptarget":newUser.target,"is_jump":False},
            2: {"jumptarget":data["url"],"is_jump":False},
            5: {"jumptarget":newUser.target,"is_jump":True},
            6: {"jumptarget":data["url"],"is_jump":True},
        }
        for one in data["textarea"]:
            try:
                temp = re.split("\.", one)[-2:]
                newOne = "www." + temp[0].strip() + "." + temp[1].strip()
            except Exception as f:
                msg = "{}无效域名,添加失败".format(one)
                msgList.append(msg)
                continue
            newJ = Jump.objects.filter(name=newOne)
            if newJ:
                newId = newJ.first().relationship_id
                if newId != data["id"]:
                    other=newJ.first().relationship.username
                    otherMsg = str(other)[:2]+"***"+str(other)[-2:]
                    msg = "警告：{}，用户：{}已添加，操作失败".format(one,otherMsg)
                    msgList.append(msg)
                    continue
                _num = int(data["mode"])
                if _num in [5,6]:
                    isJump = True
                else:
                    isJump = False
                newJ.update(name=newOne,jumptarget=regExJump[num]["jumptarget"],is_jump=isJump,relationship_id=data["id"])
            else:
                oneUserObj = User.objects.filter(id=data["id"]).first()
                JumpObjNum = len(oneUserObj.jump_target.all())
                print("oneUserObj.number",oneUserObj.number,type(oneUserObj.number))
                if (oneUserObj.number-JumpObjNum) <=0:
                    raise MyException(ref.set(403, "数量不足，无权添加"))
                Jump.objects.create(name=newOne,jumptarget=regExJump[num]["jumptarget"],is_jump=regExJump[num]["is_jump"],relationship_id=data["id"])
        if msgList:
            raise MyException(ref.set(403, msgList))
        return True

class GetJpData(View):
    """
    Jump信息获取
    """
    def get(self,request,page,size):
        userid = request.GET.get("userId",None)
        search = request.GET.get("search",None)
        # import urllib
        # print(urllib.request.unquote(r'www.sd%E4%BD%A0%E5%A5%BD.com'))
        try:
            oneUser = User.objects.get(id=userid)
        except Exception as e:
            return JsonResponse(ref.code(400))
        if all([page,size,oneUser]):
            page=int(page)
            size=int(size)
            startPage = (page-1)*size
            endPage = page*size
            jumpObj = oneUser.jump_target.all()
            if search:
                oneSer = jumpObj.filter(name=search)
                allJumps=oneSer
            else:
                allJumps = jumpObj[startPage:endPage]
            jumpList=[]
            if allJumps:
                for one in allJumps:
                    _dict = {
                        "id":one.id,
                        "name":one.name if one.name else "",
                        "jump":one.jumptarget if one.jumptarget else "",
                    }
                    jumpList.append(_dict)
            data = {
                "data":jumpList,
                "total":jumpObj.count()
            }
            data.update(ref.code(200))
            return JsonResponse(data)
        else:
            return JsonResponse(ref.code(400))

class DelJpData(View):
    """
    Jump信息删除
    """
    def delete(self,request):
        delData =request.body.decode("utf8")
        delList = json.loads(delData)
        if isinstance(delList,list):
            for i in delList:
                Jump.objects.filter(id=i["id"]).delete()
        Cache().set()
        return JsonResponse(ref.code(204))

class Logout(View):
    """
    退出
    """
    def post(self,request):
        delTk = request.META.get("HTTP_AUTHORIZATION",None)
        if delTk:
            cache.delete(delTk)
        logout(request)
        return JsonResponse({"code":200})