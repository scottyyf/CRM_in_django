#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: serializers.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""

from user_app.models import User
from rest_framework import serializers

# serializer relations
# 在序列化中，外键， manytomany, onetoone 关系中进行使用
# ModelSerializer 做基类时，只需要序列化外键的那些数据再显示声明，、
# 不用所有都显示声明
# 如果所有字段都要写, 那么使用serializers.Serializer
class UserSerializer(serializers.ModelSerializer):
    # 指向对应关系对象的 __str__方法返回值
    #serializers.StringRelatedField(many=True) # many 表示多行结果



    # 指向对应关系的pk, 比如默认的id值
    # serializers.PrimaryKeyRelatedField
    # 参数
        # queryset 做合法性校验时，查询的范围
        # read_only queryset和read_only需要设置一个
        # allow_null 是否允许控制，默认是False
        # pk_field 设置pk的 序列化和反序列化的值 pk_field=UUIDField(format='hex')

    department = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['usernmae', 'department']


    # 使用超链接表示对象关系
    # serializers.HyperlinkedRelatedField
    # tracks = serializers.HyperlinkedRelatedField，那么
    # 'tracks': [
    #     'http://www.example.com/api/tracks/45/',

    # 使用目标对象的一个field 表示关系
    # serializers.SlugRelatedField
    #


    # 自定义一个字段的读取表示方式时，继承RelatedField并重写这个方法
    # .to_representation(self, value) 实现该方法


    # department = serializers.