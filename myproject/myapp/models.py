# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import  timezone

# Create your models here.
class Account(models.Model): #用户数据库
    account_user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    # 引用了Django自身的认证系统,coursesite.auth_user这个数据库会存储用户邮箱和密码
    account_nickname = models.CharField(max_length=50)     #用户昵称
    account_cet4 = models.IntegerField(default=0)      #用户当前背到的4级单词编号
    account_cet4_today = models.IntegerField(default=0)#用户今天第一个背的四级单词编号
    account_cet6 = models.IntegerField(default=0)      #用户当前背到的6级单词编号
    account_cet6_today = models.IntegerField(default=0)  # 用户今天第一个背的六级单词编号
    account_counter = models.IntegerField(default=100) #用户背诵计划设定的单词数量,默认为100
    account_time = models.DateField(default=timezone.now)          #用户所在的日期

class Cet4(models.Model): #四级词汇表
    cet4_num = models.IntegerField()
    cet4_word = models.CharField(max_length=30)
    cet4_describe = models.CharField(max_length=150)

class Cet6(models.Model): #六级词汇表
    cet6_num = models.IntegerField()
    cet6_word = models.CharField(max_length=30)
    cet6_describe = models.CharField(max_length=150)

class Custom(models.Model): #用户自定义单词数据库
    account_id = models.IntegerField()     #用户id
    custom_num = models.IntegerField()     #单词在词汇表中的编号
    custom_catalog = models.IntegerField(default=timezone.now) #单词类型（0为四级单词，1为六级单词）