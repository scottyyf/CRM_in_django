#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: CrmAdmin.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


class CrmAdmin:
    empty_value_display = '--empty--'
    actions_on_bottom = True
    actions_on_top = False
    actions = None
    list_max_show_all = 10
    list_per_page = 10
    save_as_continue = True
    show_full_result_count = False

    # 是否有增加新条目的权限
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False

