from django.db import models

# Create your models here.
from user_app.models import User, Department


class Projects(models.Model):
    name = models.CharField(max_length=50, verbose_name='项目名称', help_text='项目名称')
    project_id = models.CharField(max_length=30, verbose_name="项目编号", primary_key=True, help_text='项目id')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建的时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')
    company = models.CharField(max_length=50, verbose_name='客户名称', help_text='客户')
    budget = models.DecimalField(max_digits=20, decimal_places=2,
                                 verbose_name='项目预算', help_text='项目预算')
    get_percent = models.DecimalField(max_digits=5, decimal_places=2,
                                      verbose_name='中标概率', help_text='中标概率')
    customer = models.CharField(max_length=25, verbose_name='客户代表', help_text='客户代表')
    tel = models.CharField(max_length=25, verbose_name='联系方式', help_text='客户联系方式')
    salesman = models.ForeignKey(User, on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 verbose_name='销售人员', help_text='销售人员',
                                 related_name='projects')
    sales_department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                         blank=True, null=True,
                                         verbose_name='销售部门', help_text='销售部门',
                                         related_name='projects')

    class Meta:
        db_table = 'sky_projects'
        ordering = ['create_time', 'name']
        verbose_name = '项目表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Processes(models.Model):
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='项目编号',
                                   help_text='项目编号', related_name='processes')
    process_issue = models.TextField(verbose_name='进度信息', help_text='进度信息')

    class Meta:
        db_table = 'sky_processes'
        verbose_name = '项目进度'
        verbose_name_plural = verbose_name

    # __str__ 在admin中的一些字段会引用，这里得是基础对象，如project_id
    def __str__(self):
        return self.project_id.project_id


class BidsInfo(models.Model):
    CHOICES = [
        (0, "投标中"),
        (1, "已中标"),
        (2, "未中标"),
        (3, "其他")
        ]
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE,
                                   null=True, blank=True, verbose_name='项目id',
                                   help_text='项目id', related_name='bids_info')
    status = models.CharField(max_length=20, choices=CHOICES,
                              verbose_name='投标状态', help_text='投标状态')
    money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='中标金额', help_text='中标金额')
    shangwu = models.ForeignKey(User, on_delete=models.CASCADE,
                                blank=True, null=True, verbose_name='商务',
                                help_text='商务', related_name='bids_info')
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='商务部门',
                                   help_text='商务部门', related_name='bids_info')
    status_desc = models.TextField(verbose_name='状态信息', help_text='状态信息')

    class Meta:
        db_table = 'sky_bids_info'
        verbose_name = '投标信息'
        verbose_name_plural = verbose_name

