# Generated by Django 4.1.3 on 2022-12-27 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_setting_semester_open_close'),
        ('users', '0016_alter_loguserroleforsemester_department_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='loguserroleforsemester',
            unique_together={('owner', 'semester_session')},
        ),
    ]
