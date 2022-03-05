from django.contrib.auth.models import AbstractUser
from django.db import models


class Myuser(AbstractUser):
    tel = models.CharField(max_length=11, verbose_name="联系方式")

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class Pinmodel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, verbose_name="模板名称")
    content = models.CharField(max_length=500, verbose_name="物品信息")
    userid = models.IntegerField(default=1, verbose_name="创建人id")
    username = models.CharField(max_length=20, verbose_name="创建人昵称")
    createtime = models.DateTimeField(auto_now=False, default=None,verbose_name='创建时间')

    class Meta:
        verbose_name = '模板管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Pinsubject(models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.CharField(max_length=22, verbose_name="拼团编码")
    name = models.CharField(max_length=40, verbose_name="拼团名称")
    userid = models.IntegerField(default=1, verbose_name="发起人ID")
    username = models.CharField(max_length=20, verbose_name="发起人昵称")
    usertel = models.CharField(max_length=11, verbose_name="发起人联系方式")
    num = models.IntegerField(default=1, verbose_name="拼团人数")
    yunum = models.IntegerField(default=0, verbose_name="余下的人数")
    pmodel = models.IntegerField(default=1, verbose_name="拼团模板ID")
    state = models.CharField(max_length=10, verbose_name="状态")
    remark = models.CharField(max_length=50, verbose_name="备注")
    createtime = models.DateTimeField(auto_now=False, default=None, verbose_name='创建时间')

    class Meta:
        verbose_name = '拼团管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Pindata(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=1, verbose_name="拼团人ID")
    username = models.CharField(max_length=20, verbose_name="拼团人昵称")
    pinid = models.CharField(max_length=22, default="", verbose_name="拼团编码")
    tel = models.CharField(max_length=11, verbose_name="联系方式")
    content = models.CharField(max_length=200, verbose_name="拼团物品")
    remark = models.CharField(max_length=50, verbose_name="备注")
    state = models.CharField(max_length=10, verbose_name="状态")
    createtime = models.DateTimeField(auto_now=False, default="2022-01-02 22:22:22", verbose_name="创建时间")

    class Meta:
        verbose_name = '订单管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


