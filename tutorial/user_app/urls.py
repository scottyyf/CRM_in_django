#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: urls.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
from django.urls import path

from user_app import views

urlpatterns = [
    path('user/info', ),
    path('user/(?P<id>[0-9]*)/info', )
    ]