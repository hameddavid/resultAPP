# Generated by Django 4.1.3 on 2023-03-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_user_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loguserroleforsemester',
            name='programme',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='programme',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
