# Generated by Django 4.1.3 on 2023-04-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0055_registration_last_score_change_by_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='last_score_change_by_ip',
            field=models.TextField(default='default'),
        ),
    ]