# Generated by Django 4.1.3 on 2023-01-10 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0007_rename_matric_number_student_stud_matric_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='matric_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='ug_reg_mat_related', to='undergraduate.student', to_field='stud_matric_number'),
        ),
    ]