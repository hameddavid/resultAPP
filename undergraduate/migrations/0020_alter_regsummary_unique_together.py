# Generated by Django 4.1.3 on 2023-02-17 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0019_rename_dpt_lecturercourse_department'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='regsummary',
            unique_together={('matric_number_fk', 'semester', 'session_id')},
        ),
    ]
