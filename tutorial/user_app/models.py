from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Department(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建的时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    name = models.CharField(max_length=25, verbose_name='部门名称', help_text='部门名称')
    parent = models.ForeignKey('self', verbose_name='上级部门',
                               on_delete=models.CASCADE,
                               null=True, blank=True, help_text='上级部门',
                               related_name='department')
    groups = models.SmallIntegerField(verbose_name='部门分组', help_text='部门分组')

    class Meta:
        verbose_name = '部门管理'
        verbose_name_plural = verbose_name
        db_table = 'sky_dpts'

    def __str__(self):
        return self.name


class Role(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建的时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    name = models.CharField(max_length=25, verbose_name='职位名称',
                            help_text='职位名称')

    class Meta:
        verbose_name = '职位'
        verbose_name_plural = verbose_name
        db_table = 'sky_roles'

    def __str__(self):
        return self.name


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'tel']
    department = models.ForeignKey(Department, verbose_name='部门',
                                   on_delete=models.CASCADE,
                                   null=True, blank=True,
                                   help_text='部门名称', related_name='user')
    job = models.ForeignKey(Role, verbose_name='职位', on_delete=models.CASCADE,
                            null=True, blank=True, help_text='职位名称', related_name='user')
    tel = models.CharField(max_length=25, verbose_name='电话',
                           help_text='电话')

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        db_table = 'sky_users'

    def __str__(self):
        return self.username
