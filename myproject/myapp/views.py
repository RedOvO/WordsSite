# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.core.exceptions import *
from django.contrib import auth
import requests
import json
from .models import * #导入所有数据库

# Create your views here.
@require_http_methods(["POST"])
@csrf_exempt
def login2(request):
    print('login')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('email')
    password = msg.get('password')

    #进行用户验证
    try:
        nowuser = User.objects.get(username=mail)
        user = auth.authenticate(username=mail, password=password)
        if user is not None:  # 用户通过验证
            if user.is_active:
                login(request=request, user=user)  # 登陆
                nickname = user.account.account_nickname
                resp = {'code': '200', 'message': 'success', 'data': {'name': nickname}}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            else:
                resp = {'code': '1034', 'message': 'Account is forbidden', 'data': {'name': 'null'}}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:  # 用户密码不正确
            resp = {'code': '1035', 'message': 'Wrong password', 'data': {'name': 'null'}}
            return HttpResponse(json.dumps(resp), content_type="application/json")
    except ObjectDoesNotExist:
        resp = {'code': '1035', 'message': 'Account does not exist', 'data': {'name': 'null'}}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(["POST"])
@csrf_exempt
def signup(request):
    print('hahaha')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('email')
    nickname = msg.get('name')
    password = msg.get('password')

    #检查用户名合密码长度
    if len(password) < 6:
        resp = {'code': '1030', 'message': 'password too short', 'data': 'false'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    if len(password) > 21:
        resp = {'code': '1031', 'message': 'password too long', 'data': 'false'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    if len(nickname) < 1:
        resp = {'code': '1032', 'message': 'username too short', 'data': 'false'}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    if len(nickname) > 21:
        resp = {'code': '1033', 'message': 'username too long', 'data': 'false'}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    #判断用户名是否已存在
    temp = User.objects.filter(username=mail)
    if temp:
        resp = {'code': '1034', 'message': 'email exsits', 'data': 'false'}
    else:
        newuser = User.objects.create_user(username=mail, password=password)  # 存入User数据库中。
        Account.objects.create(account_user=newuser, account_nickname=nickname)  # 存入Account数据库中
        resp = {'code': '200', 'message': 'success', 'data': 'true'}

    return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(["POST"])
@csrf_exempt
def cet4(request):
    print(request.POST)  # 打印收到的json信息
    response = {}
    resp = {'errorcode': 100, 'detail': 'Get success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")

    # return JsonResponse(response)

@require_http_methods(["GET"])
def cet6(request):
    response = {}
    # try:
    #     books = Book.objects.filter()
    #     response['list']  = json.loads(serializers.serialize("json", books))
    #     response['msg'] = 'success'
    #     response['error_num'] = 0
    # except  Exception as e:
    #     response['msg'] = str(e)
        # response['error_num'] = 1

    return JsonResponse(response)
