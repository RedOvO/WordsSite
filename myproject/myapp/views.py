# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.contrib import auth
import requests
import json
import random
import datetime
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
                setting = user.account.account_setting
                resp = {'code': '200', 'message': 'success', 'data': {'name': nickname, 'setting': setting}}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            else:
                resp = {'code': '1034', 'message': 'Account is forbidden', 'data': {'name': 'null'}}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:  # 用户密码不正确
            resp = {'code': '1035', 'message': 'Wrong password', 'data': {'name': 'null'}}
            return HttpResponse(json.dumps(resp), content_type="application/json")
    except ObjectDoesNotExist:
        resp = {'code': '1036', 'message': 'Account does not exist', 'data': {'name': 'null'}}
        return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(["POST"])
@csrf_exempt
def signup(request):
    print('signup')
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
def logout2(request):
    print('logout')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('email')
    logout(request) #登出
    resp = {'code': '200', 'message': 'success', 'data': 'true'}

    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(["POST"])
@csrf_exempt
def recite_cet4(request):
    print('recite cet4')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)
    num = nowuser.account_cet4  # 当前背诵的单词编号

    if num == 0:
        nowuser.account_cet4 = 1
        nowuser.save()

    # 判断用户是否为当天第一次背4级单词
    if nowuser.account_time != datetime.date.today():
        nowuser.account_time = datetime.date.today()
        nowuser.account_cet4_today = 0
        nowuser.account_cet6_today = 0
        nowuser.save()

    # 若用户是当天第一次使用背4级单词，使当天第一个单词编号与当前单词编号相同
    if nowuser.account_cet4_today == 0:
        nowuser.account_cet4_today = nowuser.account_cet4
        nowuser.save()

    # 获取单词
    aword = Cet4.objects.get(cet4_num=nowuser.account_cet4)
    word = aword.cet4_word
    desc = aword.cet4_describe
    print(word)
    try:
        custom = Custom.objects.get(account_id=nowuser.account_user_id, custom_num=nowuser.account_cet4, custom_catalog=0)
        collected = True
    except ObjectDoesNotExist:
        print(word + 'is not collected')
        collected = False

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'counter': nowuser.account_counter,  # 背诵计划设置的量
            'present_no': nowuser.account_cet4,  # 应该背诵的第一个单词的序号
            'today_no': nowuser.account_cet4_today,  # 今天应该背诵的第一个单词的序号
            'today_words': {
                'word': word,
                'desc': desc,
                'collected': collected
            }  # 今天第一个要背诵的单词
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(["POST"])
@csrf_exempt
def recite_cet6(request):
    print('recite cet6')  # 打印收到的json信息
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)
    num = nowuser.account_cet6        #当前背诵的单词编号

    if num == 0:
        nowuser.account_cet6 = 1
        nowuser.save()

    #判断用户是否为当天第一次背6级单词
    if nowuser.account_time != datetime.date.today():
        nowuser.account_time = datetime.date.today()
        nowuser.account_cet4_today = 0
        nowuser.account_cet6_today = 0
        nowuser.save()

    #若用户是当天第一次使用背6级单词，使当天第一个单词编号与当前单词编号相同
    if nowuser.account_cet6_today == 0:
        nowuser.account_cet6_today = nowuser.account_cet6
        nowuser.save()

    #获取单词
    aword = Cet6.objects.get(cet6_num=nowuser.account_cet6)
    word = aword.cet6_word
    desc = aword.cet6_describe
    print(word)
    try:
        custom = Custom.objects.get(account_id=nowuser.account_user_id, custom_num=nowuser.account_cet6, custom_catalog=1)
        collected = True
    except ObjectDoesNotExist:
        print(word + 'is not collected')
        collected = False

    resp = {
        'code': '200',
        'message': 'success',
	    'data':{
            'counter':    nowuser.account_counter,   #背诵计划设置的量
            'present_no': nowuser.account_cet6,      # 应该背诵的第一个单词的序号
            'today_no':   nowuser.account_cet6_today,#今天应该背诵的第一个单词的序号
            'today_words': {
                'word': word,
                'desc': desc,
                'collected': collected
            }  # 今天第一个要背诵的单词
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(["POST"])
@csrf_exempt
def cet4_next(request):
    print('next cet4')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    present_no = msg.get('present_no')
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    nowuser.account_cet4 = present_no + 1
    if nowuser.account_cet4 > 5520:
        nowuser.account_cet4 = 1
        nowuser.account_cet4_today = 1
    nowuser.save()

    # 获取单词
    aword = Cet4.objects.get(cet4_num=nowuser.account_cet4)
    word = aword.cet4_word
    desc = aword.cet4_describe
    print(word)
    try:
        custom = Custom.objects.get(account_id=nowuser.account_user_id, custom_num=nowuser.account_cet4, custom_catalog=0)
        collected = True
    except ObjectDoesNotExist:
        print(word + 'is not collected')
        collected = False

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'present_no': nowuser.account_cet4,  # 当前背诵的单词序号
            'today_words': {
                'word': word,
                'desc': desc,
                'collected': collected
            }  # 今天第一个要背诵的单词
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")


@require_http_methods(["POST"])
@csrf_exempt
def cet6_next(request):
    print('next cet6')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    present_no = msg.get('present_no')
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    nowuser.account_cet6 = present_no + 1
    if nowuser.account_cet6 > 1540:
        nowuser.account_cet6 = 1
        nowuser.account_cet6_today = 1
    nowuser.save()

    # 获取单词
    aword = Cet6.objects.get(cet6_num=nowuser.account_cet6)
    word = aword.cet6_word
    desc = aword.cet6_describe
    print(word)
    try:
        custom = Custom.objects.get(account_id=nowuser.account_user_id, custom_num=nowuser.account_cet6, custom_catalog=1)
        collected = True
    except ObjectDoesNotExist:
        print(word + 'is not collected')
        collected = False

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'present_no': nowuser.account_cet6,  # 当前背诵的单词序号
            'today_words': {
                'word': word,
                'desc': desc,
                'collected': collected
            }  # 今天第一个要背诵的单词
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def collect(request):
    print('custom words collect')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    present_no = msg.get('present_no')
    catalog = msg.get('catalog')

    #获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    #存入Custom数据库
    Custom.objects.create(account_id=nowuser.account_user_id, custom_num=present_no, custom_catalog=catalog)
    resp = {'code': '200', 'message': 'success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def delete(request):
    print('custom words delete')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    word = msg.get('word')
    catalog = msg.get('catalog')

    #获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    #获取单词编号
    if catalog == 0: #单词为4级
        aword = Cet4.objects.get(cet4_word=word)
        num=aword.cet4_num
    elif catalog == 1: #单词为6级
        aword = Cet6.objects.get(cet6_word=word)
        num=aword.cet6_num

    #删除对应自定义单词
    Custom.objects.get(account_id=nowuser.account_user_id, custom_num=num, custom_catalog=catalog).delete()


    resp = {'code': '200', 'message': 'success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def cet4_list(request):
    print('get cet4 list')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')

    # 获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    #构建一个列表，列表里为所有的自定义六级单词
    try:
        custom = Custom.objects.filter(account_id=nowuser.account_user_id, custom_catalog=0)
        print(custom)
        wordslist = []
        for item in custom:
            word = Cet4.objects.get(cet4_num=item.custom_num)
            wordslist = wordslist + [{'word': word.cet4_word, 'desc': word.cet4_describe, 'catalog': 0}]
    except ObjectDoesNotExist:
        wordslist = []

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'words_list': wordslist
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def cet6_list(request):
    print('get cet6 list')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')

    # 获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    #构建一个列表，列表里为所有的自定义六级单词
    try:
        custom = Custom.objects.filter(account_id=nowuser.account_user_id, custom_catalog=1)
        print(custom)
        wordslist = []
        for item in custom:
            word = Cet6.objects.get(cet6_num=item.custom_num)
            wordslist = wordslist + [{'word': word.cet6_word, 'desc': word.cet6_describe, 'catalog': 1}]
    except ObjectDoesNotExist:
        wordslist = []

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'words_list': wordslist
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def cet4_review_test(request):
    print('cet4 review/test')
    print(request.POST)
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')

    # 获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    wordslist = []
    if nowuser.account_cet4 < 101:
        words = Cet4.objects.all()[:nowuser.account_cet4]  # 用户学习过的单词少于100个，返回所有学习过的单词
        print(words)
        for item in words:
            word = Cet4.objects.get(cet4_num=item.cet4_num)
            wordslist = wordslist + [{'word': word.cet4_word, 'desc': word.cet4_describe, 'catalog': 1}]
    else:
        rand_word = random.sample(range(1, nowuser.account_cet4), 100)
        for id in rand_word:
            word = Cet4.objects.get(cet4_num=id)  # 多于100个，随机返回100个
            wordslist = wordslist + [{'word': word.cet4_word, 'desc': word.cet4_describe, 'catalog': 1}]

    #构建要返回的100个单词列表
    #wordslist = []
    #for item in words:
    #    word = Cet4.objects.get(cet4_num=item.cet4_num)
    #    wordslist = wordslist + [{'word': word.cet4_word, 'desc': word.cet4_describe, 'catalog': 0}]

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'words_list': wordslist
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def cet6_review_test(request):
    print('cet6 review/test')
    print(request.POST)
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')

    # 获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    wordslist = []
    if nowuser.account_cet6 < 101:
        words = Cet6.objects.all()[:nowuser.account_cet6] #用户学习过的单词少于100个，返回所有学习过的单词
        print(words)
        for item in words:
            word = Cet6.objects.get(cet6_num=item.cet6_num)
            wordslist = wordslist + [{'word': word.cet6_word, 'desc': word.cet6_describe, 'catalog': 1}]
    else:
        rand_word = random.sample(range(1, nowuser.account_cet6), 100)
        for id in rand_word:
            word = Cet6.objects.get(cet6_num=id)   #多于100个，随机返回100个
            wordslist = wordslist + [{'word': word.cet6_word, 'desc': word.cet6_describe, 'catalog': 1}]



    #构建要返回的100个单词列表
    # wordslist = []
    # for item in words:
    #     word = Cet6.objects.get(cet6_num=item.cet6_num)
    #     wordslist = wordslist + [{'word': word.cet6_word, 'desc': word.cet6_describe, 'catalog': 1}]

    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'words_list': wordslist
        }
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(['POST'])
@csrf_exempt
def setting(request):
    print('setting')
    dic = list(request.POST)[0]
    msg = json.loads(dic)
    mail = msg.get('user')
    counter = msg.get('counter')
    setting = msg.get('setting')

    # 获取用户id
    present_user = User.objects.get(username=mail)
    nowuser = Account.objects.get(id=present_user.id)

    #更改设置信息
    if nowuser.account_counter != counter:
        nowuser.account_counter = counter
    if nowuser.account_setting != setting:
        nowuser.account_setting = setting
    nowuser.save()

    resp = {'code': '200', 'message': 'success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")

