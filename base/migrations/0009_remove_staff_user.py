# Generated by Django 4.1.3 on 2023-01-20 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_setting_semester_open_close'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='user',
        ),
    ]