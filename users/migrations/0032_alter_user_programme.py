# Generated by Django 4.1.3 on 2023-03-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_alter_loguserroleforsemester_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='programme',
            field=models.CharField(max_length=30),
        ),
    ]
