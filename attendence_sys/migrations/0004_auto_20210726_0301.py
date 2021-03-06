# Generated by Django 3.0.14 on 2021-07-26 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendence_sys', '0003_auto_20210725_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='department',
            field=models.CharField(choices=[('Select Department', 'Select Department'), ('Department of Agricultural Economics', 'Department of Agricultural Economics'), ('Department of Animal Science', 'Department of Animal Science'), ('Department of Horticulture', 'Department of Horticulture')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL),
        ),
    ]
