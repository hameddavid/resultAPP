# Generated by Django 4.1.3 on 2023-03-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0025_remove_programme_programme_id_programme_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturercourse',
            name='department',
            field=models.CharField(max_length=45),
        ),
    ]