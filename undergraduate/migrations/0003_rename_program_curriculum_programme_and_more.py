# Generated by Django 4.1.3 on 2022-12-30 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0002_alter_curriculum_program_alter_curriculum_semester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='curriculum',
            old_name='program',
            new_name='programme',
        ),
        migrations.AlterUniqueTogether(
            name='curriculum',
            unique_together={('programme', 'course_code')},
        ),
    ]
