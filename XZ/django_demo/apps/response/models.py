# -*- coding: UTF-8 -*-
from django.db import models


# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=10, default='', primary_key=True, verbose_name='主键')
    name = models.CharField(max_length=8, verbose_name=u'用户名', null=True, blank=True, default='')
    email = models.EmailField(verbose_name=u'邮箱', null=True, blank=True)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
        db_table = 'user_info'
        ordering = ['user_id']
