# Generated by Django 4.1.3 on 2023-01-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0008_registration_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='unit',
            field=models.IntegerField(default=0),
        ),
    ]
