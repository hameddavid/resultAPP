# Generated by Django 4.1.3 on 2023-01-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0011_alter_registration_matric_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='matric_number',
            field=models.CharField(max_length=45),
        ),
    ]
