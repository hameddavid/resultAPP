# Generated by Django 4.1.3 on 2023-03-20 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0028_alter_curriculum_programme_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programme',
            old_name='programme_id',
            new_name='programme_code',
        ),
    ]