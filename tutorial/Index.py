#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: Index.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
from django.utils.text import capfirst
from django.contrib import admin
from collections import OrderedDict as SortedDict


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count += 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        template_response = func(*args, **kwargs)
        for app in template_response.context_data['app_list']:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return template_response

    return inner
