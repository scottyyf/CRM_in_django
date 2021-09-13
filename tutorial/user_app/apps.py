from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    # 展示选项条目的名称，而不用user_app
    # 首页 › 用户级别管理 › 用户管理 › admin
    verbose_name = '1. 用户级别管理'
