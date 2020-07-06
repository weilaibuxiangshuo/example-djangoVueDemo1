# -*- coding:utf-8 -*-
from django.urls import re_path,path


from .views import (Login,Logout,MgUser,GetUser,DelUser,GetData,\
    JpData,GetJpData,DelJpData,UserInfo)


app_name="new"
urlpatterns=[
    re_path(r'^login/$',Login.as_view(),name="login"),
    re_path(r'^userinfo/$',UserInfo.as_view(),name="userinfo"),
    re_path(r'^getuser/(\d+)/(\d+)/$',GetUser.as_view(),name="getuser"),
    re_path(r'^mguser/$',MgUser.as_view(),name="mguser"),
    re_path(r'^deluser/$',DelUser.as_view(),name="deluser"),
    re_path(r'^getdata/$',GetData.as_view(),name="getdata"),
    re_path(r'^jpdata/$',JpData.as_view(),name="jpdata"),
    re_path(r'^getjpdata/(\d+)/(\d+)/$',GetJpData.as_view(),name="getjpdata"),
    re_path(r'^deljpdata/$',DelJpData.as_view(),name="deljpdata"),
    re_path(r'^logout/$',Logout.as_view(),name="logout"),
]