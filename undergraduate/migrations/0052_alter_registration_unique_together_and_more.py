# Generated by Django 4.1.3 on 2023-03-26 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0051_alter_student_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='regsummary',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='registration',
            name='matric_number_fk',
        ),
        migrations.RemoveField(
            model_name='regsummary',
            name='matric_number_fk',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
