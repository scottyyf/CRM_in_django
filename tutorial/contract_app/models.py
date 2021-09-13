from django.db import models

# Create your models here.
from project_app.models import Projects


class Contract(models.Model):
    ACCEPTED = [
        (0, '未验收'),
        (1, '已验收')
        ]
    code = models.CharField(max_length=50, verbose_name='合同编号', help_text='合同编号')
    name = models.CharField(max_length=50, verbose_name='合同名称', help_text='合同名称')
    money = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='合同金额',
                                help_text='合同金额')
    buyer = models.CharField(max_length=25, verbose_name='客户名称', help_text='客户名称')
    contact_man = models.CharField(max_length=25, verbose_name='联系人', help_text='联系人')
    contact_way = models.CharField(max_length=25, verbose_name='联系方式', help_text='练习方式')
    sign_at = models.DateTimeField(auto_now_add=True, verbose_name='签订时间', help_text='签订时间')
    is_accepted = models.SmallIntegerField(choices=ACCEPTED, max_length=20, verbose_name='交货验收',
                                   help_text='交货验收')
    accepted_info = models.TextField(verbose_name='验收信息', help_text='验收信息')
    project_id = models.OneToOneField(Projects, verbose_name='项目id', on_delete=models.CASCADE,
                                      related_name='contract_info', null=True, blank=True)

    class Meta:
        db_table = 'sky_contracts'
        verbose_name = '合同'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PayInfo(models.Model):
    CHOICE = [
        (0, '现金'),
        (1, '股票'),
        (2, '抵押'),
        (3, '货物交换'),
        ]
    pay_method = models.CharField(max_length=20, choices=CHOICE, verbose_name='回款方式',
                                  help_text='货款方式')
    pay_message = models.TextField(help_text='备注', verbose_name='备注')
    need_pay = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='待收款',
                                   help_text='待收款')
    already_pay = models.DecimalField(max_digits=20, decimal_places=2,verbose_name='回款',
                                      help_text='回款')
    pay_time = models.DateTimeField(verbose_name='回款时间', help_text='回款时间')
    contract_id = models.ForeignKey(Contract, on_delete=models.CASCADE,
                                    null=True, blank=True, related_name='pay_info',
                                    verbose_name='合同编号', help_text='合同编号',
                                    )

    class Meta:
        db_table = 'sky_pay_info'
        verbose_name = '回款信息'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.
