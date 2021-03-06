# Generated by Django 3.2.6 on 2021-09-13 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0003_auto_20210913_0148'),
        ('contract_app', '0002_alter_contract_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='project_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_info', to='project_app.projects', verbose_name='项目id'),
        ),
    ]
