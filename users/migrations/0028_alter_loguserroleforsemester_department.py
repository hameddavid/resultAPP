# Generated by Django 4.1.3 on 2023-03-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_alter_loguserroleforsemester_programme_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loguserroleforsemester',
            name='department',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
