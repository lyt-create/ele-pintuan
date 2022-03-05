from django.contrib import admin
from .import models
# Register your models here.
# admin.site.register(models.Myuser)#后台能显示表数据
class MyuserAdmin(admin.ModelAdmin):#定义一个类，显示列表数据
    search_fields = ['username']#根据某字段搜索
    list_filter =['username']#过滤器，根据字段进行筛选
admin.site.register(models.Myuser, MyuserAdmin)

class PinmodelAdmin(admin.ModelAdmin):#定义一个类，显示列表数据
    search_fields = ['name']#根据某字段搜索
    list_filter =['name']#过滤器，根据字段进行筛选
admin.site.register(models.Pinmodel, PinmodelAdmin)

class PinsubjectAdmin(admin.ModelAdmin):#定义一个类，显示列表数据
    search_fields = ['name']#根据某字段搜索
    list_filter =['name']#过滤器，根据字段进行筛选
admin.site.register(models.Pinsubject, PinsubjectAdmin)

class PindataAdmin(admin.ModelAdmin):#定义一个类，显示列表数据
    search_fields = ['username']#根据某字段搜索
    list_filter =['username']#过滤器，根据字段进行筛选
admin.site.register(models.Pindata, PindataAdmin)