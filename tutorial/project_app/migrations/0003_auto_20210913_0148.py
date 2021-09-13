# Generated by Django 3.2.6 on 2021-09-13 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0002_alter_bidsinfo_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidsinfo',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0, help_text='中标金额', max_digits=10, verbose_name='中标金额'),
        ),
        migrations.AlterField(
            model_name='bidsinfo',
            name='status_desc',
            field=models.TextField(default='null', help_text='状态信息', verbose_name='状态信息'),
        ),
    ]