# Generated by Django 3.0.14 on 2021-07-25 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendence_sys', '0002_auto_20210725_2020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name_plural': 'Teachers'},
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='students',
        ),
        migrations.AddField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Teachers'),
        ),
    ]