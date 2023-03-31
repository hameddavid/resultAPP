# Generated by Django 4.1.3 on 2023-03-26 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('undergraduate', '0041_remove_student_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registration',
            name='matric_number_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_reg_stud_related', to='undergraduate.student', to_field='matric_number'),
        ),
        migrations.AlterField(
            model_name='regsummary',
            name='matric_number_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='ug_reg_sum_related', to='undergraduate.student', to_field='matric_number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='matric_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
