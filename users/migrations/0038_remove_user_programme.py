# Generated by Django 4.1.3 on 2023-03-20 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_alter_leveladviser_programme_alter_user_programme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='programme',
        ),
    ]