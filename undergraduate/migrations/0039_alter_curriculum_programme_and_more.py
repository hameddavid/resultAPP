# Generated by Django 4.1.3 on 2023-03-21 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0038_alter_curriculum_programme_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='programme',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='lecturercourse',
            name='programme',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
