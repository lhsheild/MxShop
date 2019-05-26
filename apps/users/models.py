from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """
    用户表
    """
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), max_length=8, default='male', verbose_name='性别')
    mobile = models.CharField(max_length=13, verbose_name='电话', null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            # 如果不为空则返回用户名
            return self.name
        else:
            # 如果用户名为空则返回不能为空的对象
            return str(self.username)


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField(max_length=60, verbose_name='验证码')
    type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码')), max_length=8, verbose_name='验证码类型')
    mobile = models.CharField(max_length=13, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
