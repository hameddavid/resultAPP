# Generated by Django 4.1.3 on 2023-03-20 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0036_alter_programme_created_alter_programme_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ug_curriculum_program_related', to='undergraduate.programme', to_field='programme_code'),
        ),
        migrations.AlterField(
            model_name='lecturercourse',
            name='programme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='undergraduate.programme', to_field='programme_code'),
        ),
    ]
