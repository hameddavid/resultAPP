# Generated by Django 4.1.3 on 2023-04-27 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0054_registration_matric_number_fk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='last_score_change_by_ip',
            field=models.CharField(default='default', max_length=30),
        ),
        migrations.AddField(
            model_name='registration',
            name='score_history',
            field=models.TextField(default='default'),
        ),
    ]